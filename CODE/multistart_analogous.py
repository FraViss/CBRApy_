import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint,solve_ivp
from scipy.optimize import minimize,optimize
import matplotlib.pyplot as plt
from functions_repository import odefun,cost_function,fmincon_py

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

def random_point(params_lb_log, params_ub_log):
    return np.random.uniform(params_lb_log, params_ub_log)

def multistart(cost_function, N, params_lb_log, params_ub_log, t_data, data):
    x_star = None
    f_star = np.inf

    for i in range(N):
        print(f"Starting iteration {i + 1}")  # Check that the loop is running

        x_0 = random_point(params_lb_log, params_ub_log)
        print("start point ", i+1, ": ", np.power(x_0,10))
        func = lambda x_0: cost_function(t_data, x_0, data)
        out = fmincon_py(func, params_init_log=x_0, params_lb_log=params_lb_log, params_ub_log=params_ub_log,disp=False)

        print(f"Optimizer finished, success: {out['success']}")  # Check that the optimizer is running
        if out["success"] and out["fun"] < f_star:
            x_star = out["opt_params"]
            f_star = out["fun"]

        print(f'Iteration: {i + 1}, Best cost so far: {f_star}, Best params so far: {x_star}')

    print("Optimal parameters:", x_star)
    print("Minimal cost:", f_star)

    return x_star, f_star


# Perform the multistart optimization
params_optimal, minimal_cost = multistart(cost_function, 10, params_lb_log, params_ub_log, time, data)

'''
test di random_point
1. verifica dei bound 
2. matlab come funziona il random_point in multistart?
3. np.random.uniform trova punti sempre diversi?

multistart_py deve dirmi quante esecuzioni hanno avuto successo e dirmi a che punto è passo passo
"sono all'esecuzione 1 di 7 e i miei punti iniziali sono... il valore calcolato è... i parametri calcolati sono..."
'''