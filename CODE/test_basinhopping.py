import numpy as np
from scipy.optimize import basinhopping, Bounds
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from functions_repository import odefun,objective_func

# Parameters and initial conditions
data = np.array([1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410])  # array concentration troponin
tempo = np.array([5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167])  # array acquisition times troponin
parameter_init = np.array([0.005, 0.005, 30, 0.1, 1])

lb = np.array([0.001, 0.001, 20, 0.001, 0.1])  # lower bounds
ub = np.array([5, 5, 300, 200, 400])  # upper bounds

params_init_log = np.log10(parameter_init)

# Lower and Upper Bounds
params_lb_log = np.log10(lb)
params_ub_log = np.log10(ub)

bounds = Bounds(params_lb_log, params_ub_log)

func = lambda params_init_log: objective_func(params_init_log, data, tempo)
# Optimization using Basin-hopping
minimizer_kwargs = {"method": "L-BFGS-B", "bounds": bounds}
result = basinhopping(func, params_init_log, minimizer_kwargs=minimizer_kwargs, niter=100, stepsize=5.0,disp=True)

# Optimized parameters
best_params = result.x
print(best_params)

x0_best = np.array([best_params[-2], best_params[-1], 0])
t_vec_stemi = np.linspace(0, tempo[-1]*1.6, 201)

# Solve ODE
X_stemi = odeint(lambda x, t: odefun(t, x, best_params), x0_best, t_vec_stemi)

# Plot
plt.figure(1)
plt.plot(t_vec_stemi, X_stemi[:, 2])
plt.show()

# Show value
value = func(best_params)
print(value)