import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.interpolate as sp_interp
import scipy.integrate as sp_integrate
from pyomo.core import Objective, Var, ConcreteModel
from pyomo.opt import SolverFactory
from scipy.integrate import odeint
from pyomo.environ import RealSet
from eq_diff_solver import odefun


x0=np.array([7,3,0])
params_log=[1,1,0]
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina
lb = [0.001, 0.001, 20, 0.001, 0.1] #lower bound
ub = [5, 5, 300, 200, 400] #upper bound
globalfunction = 'MultiStart' # oppure 'particleswarm'
localfunction = 'fmincon'
parameter_init = [0.005, 0.005, 30, 0.1, 1] # parametri iniziali
number_point = 1 # %40 %25 1

def obj_troponinModel(params_log, data, time):
    t = np.linspace(0, max(time) * 1.6, 201)
    params_log = np.array([10 ** p if p is not None and not np.isnan(p) else None for p in params_log])

    # Check if params contains None values
    if np.any(params_log is None):
        raise ValueError("Invalid parameter values")

    x0 = [params_log[-2], params_log[-1], 0]
    X = odeint(odefun, x0, t, args=(params_log,))
    cTnT_sim = sp_interp.interp1d(t + params_log[-1], X[:, 2], time)
    obj = np.sum(np.power(data - cTnT_sim(time), 2) * data)
    return obj


def troponin_model(data, tempo, parameter_init, lb, ub):
    t_vec_stemi = np.linspace(0, int(max(tempo)+50), int(max(tempo)+51))
    params_init_log = np.log10(parameter_init)
    params_lb_log = np.log10(lb)
    params_ub_log = np.log10(ub)

    # Define a Pyomo ConcreteModel
    model = ConcreteModel()

    # Define decision variables
    model.param1 = Var(domain=RealSet, bounds=(params_lb_log[0], params_ub_log[0]))
    model.param2 = Var(domain=RealSet, bounds=(params_lb_log[1], params_ub_log[1]))

    # Define the objective function
    model.obj = Objective(expr=obj_troponinModel(np.array([model.param1.value, model.param2.value]), data, tempo))

    # Solve the optimization problem
    solver = SolverFactory('ipopt')
    solver.solve(model)

    # Retrieve the optimal parameter values
    opt_param1 = 10 ** model.param1.value
    opt_param2 = 10 ** model.param2.value

    x0 = [opt_param1, opt_param2, 0]
    print('Solving model')
    T_stemi, X_stemi = odeint(odefun, x0, t_vec_stemi, args=(np.array([opt_param1, opt_param2]),))
    return [T_stemi, X_stemi, [opt_param1, opt_param2]]


def plot_troponin_results(T_stemi, X_stemi):
    plt.plot(T_stemi, X_stemi[:, 0], label='Variable 1')
    plt.plot(T_stemi, X_stemi[:, 1], label='Variable 2')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

# Call the troponin_model function and retrieve the results
results = troponin_model(data, time, parameter_init, lb, ub)
T_stemi, X_stemi, opt_params = results

# Plot the results
plot_troponin_results(T_stemi, X_stemi)