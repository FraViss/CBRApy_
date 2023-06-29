import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sp_interp
from scipy.integrate import odeint
from pyomo.environ import ConcreteModel, Var, Objective
from pyomo.opt import SolverFactory
from pyomo.environ import RealSet, Reals

t = np.linspace(0, 10, 100)
x = np.array([7, 3, 0])
params_log = np.array([1, 1, 0])
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]
lb = [0.001, 0.001, 20, 0.001, 0.1]
ub = [5, 5, 300, 200, 400]
parameter_init = [0.005, 0.005, 30, 0.1, 1]

def odefun(x, t, params_log):
    # Variables
    Cs_ctnt = x[0]
    Cc_ctnt = x[1]
    Cp_ctnt = x[2]

    # Arguments
    a_log = params_log[0]
    b_log = params_log[1]
    Tsc_log = params_log[2]

    # cTnT
    Jsc_ctnt = Cs_ctnt - Cc_ctnt
    Jcp_ctnt = np.power(10, a_log) * (Cc_ctnt - Cp_ctnt)
    Jpm_ctnt = np.power(10, b_log) * Cp_ctnt

    # sigmoid curve
    G_sc = np.power(t, 3) / (np.power(t, 3) + np.power(10, (3 * Tsc_log)))

    # Differential equations
    dCs_ctnt_tau = - Jsc_ctnt * G_sc
    dCc_ctnt_tau = Jsc_ctnt * G_sc - Jcp_ctnt
    dCp_ctnt_tau = Jcp_ctnt - Jpm_ctnt

    # Result
    d_concentration = [dCs_ctnt_tau, dCc_ctnt_tau, dCp_ctnt_tau]

    return d_concentration


def obj_troponinModel(params_log, data, time):
    t = np.linspace(0, max(time) * 1.6, 201)
    params_log = np.array([10 ** p for p in params_log])

    x0 = np.array([params_log[0], params_log[1], params_log[2]])
    X = odeint(odefun, x0, t, args=(params_log,))
    cTnT_sim = sp_interp.interp1d(t + params_log[-1], X[:, 2], kind='cubic',bounds_error=False) # approfondire interp1d # test linear e quadratic
    obj = np.sum(np.power(data - cTnT_sim(time), 2)*data) # questa operazione va rivista aggiungere moltiplicazione per data
    return obj

def troponin_model(data, tempo, parameter_init, lb, ub):
    t_vec_stemi = np.linspace(0, int(max(tempo) + 50), int(max(tempo) + 51))
    params_init_log = np.log10(parameter_init)
    params_lb_log = np.log10(lb)
    params_ub_log = np.log10(ub)

    # Define a Pyomo ConcreteModel
    model = ConcreteModel()

    # Define decision variables
    model.param0 = Var(domain=Reals, bounds=(params_lb_log[0], params_ub_log[0]), initialize=params_init_log[0])
    model.param1 = Var(domain=Reals, bounds=(params_lb_log[1], params_ub_log[1]), initialize=params_init_log[1])
    model.param2 = Var(domain=Reals, bounds=(params_lb_log[2], params_ub_log[2]), initialize=params_init_log[2])

    def obj_rule(model):
        return obj_troponinModel(np.array([model.param0.value, model.param1.value, model.param2.value]), data, tempo)

    # Define the objective function
    model.obj = Objective(rule=obj_rule)

    # Solve the optimization problem
    solver = SolverFactory('multistart') # ipopt da impostare
    solver.solve(model)

    # Retrieve the optimal parameter values
    opt_param1 = 10 ** model.param1.value
    opt_param2 = 10 ** model.param2.value

    x0 = np.array([opt_param1, opt_param2, 0])
    T_stemi, X_stemi = odeint(odefun, x0, t_vec_stemi, args=(np.array([opt_param1, opt_param2, 0]),))
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

#Scipy e pyomo non si parlano: la prima fa calcolo numerico e la seconda fa calcolo simbolico.
#alternative: jax, pytorch?
#no! solo scipy.