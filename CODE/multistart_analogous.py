import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint,solve_ivp
from scipy.optimize import minimize,optimize
import matplotlib.pyplot as plt
from functions_repository import odefun,cost_function

#Test
#params = [0.0050, 0.0050, 67.6505, 0.1000, 1.0000]
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina
parameter_init=[0.005, 0.005, 30, 0.1, 1]

params_init_log = np.log10(parameter_init)

# Bounds
lb = [0.001, 0.001, 20, 0.001, 0.1]  # lower bounds
ub = [5, 5, 300, 200, 400]  # upper bounds
params_lb_log = np.log10(lb)
params_ub_log = np.log10(ub)

def multistart(cost_function, N, params_lb_log, params_ub_log, t_data, data):
    x_star = None
    f_star = np.inf

    for i in range(N):
        print(f"Starting iteration {i + 1}")  # Check that the loop is running

        x_0 = random_point(params_lb_log, params_ub_log)
        result = minimize(cost_function, x_0, args=(t_data, data), method='SLSQP')

        print(f"Optimizer finished, success: {result.success}")  # Check that the optimizer is running
        if result.success and result.fun < f_star:
            x_star = result.x
            f_star = result.fun

        print(f'Iteration: {i + 1}, Best cost so far: {f_star}, Best params so far: {x_star}')

    return x_star, f_star

def random_point(params_lb_log, params_ub_log):
    return np.random.uniform(params_lb_log, params_ub_log)

# Perform the multistart optimization
params_optimal, minimal_cost = multistart(cost_function, 10, params_lb_log, params_ub_log, time, data)
print("Optimal parameters:", params_optimal)
print("Minimal cost:", minimal_cost)