import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint
import scipy as sp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from functions_repository import odefun, const_func0


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


# Optimization problem
problem = {
    'fun': lambda parameter_init: const_func0(parameter_init, data, time),
    'x0': params_init_log,
    'bounds': list(zip(params_lb_log, params_ub_log)),
    'method': 'SLSQP',
    'options': {'maxiter': 1000}
}

# Solve the optimization problem
result = minimize(**problem)

sol = result.x

print("Result: ", result.x)
print("Success: ", result.success)
print("Status: ", result.status)
print("Message: ", result.message)

# Get the optimized parameters
params_opt = 10 ** sol

# Simulate the model using the optimized parameters
x0 = [params_opt[-2], params_opt[-1], 0]
t_sim = np.linspace(0, time[-1] * 1.6, 201)
X_sim = odeint(lambda x, t: odefun(x, t, params_opt), x0, t_sim)
cTnT_sim = sp_interp.interp1d(t_sim, X_sim[:, 2])(time)

# Plot the results
plt.plot(time, data, '-', label='Experimental data')
plt.plot(time, cTnT_sim, label='Model simulation')
plt.xlabel('Time')
plt.ylabel('Concentration of troponin')
plt.legend()
plt.show()

'''
add = lambda x, y: x + y

print(add(5, 3))  # Prints 8
'''