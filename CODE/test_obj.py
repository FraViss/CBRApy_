import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint,solve_ivp
from scipy.optimize import minimize,basinhopping
import matplotlib.pyplot as plt
from functions_repository import odefun,obj_func

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

func = lambda params_init_log: obj_func(params_init_log, data, time)
# Optimization problem

problem = {
    'fun': func,
    'x0': params_init_log,
    'bounds': list(zip(params_lb_log, params_ub_log)),
    'method': 'SLSQP',
    'options': {'maxiter': 1000,"disp":True}
}

# Solve the optimization problem
result = minimize(**problem)

sol = result.x
best_params_linear = np.power(10, sol)

print("Optimal parameters: ", result.x)
print("Success: ", result.success)
print("Status: ", result.status)
print("Message: ", result.message)
#Test
value=obj_func(result.x,data,time)
print("Test: ",value)

'''
# Get the optimized parameters
params_opt = 10 ** sol
best_params=[0.5941, 0.095959, 70.1804, 7.058, 3.2886]
# Simulate the model using the optimized parameters
x0 = [params_opt[-2], params_opt[-1], 0]
t_sim = np.linspace(0, time[-1] * 1.6, 201)
#X_sim = odeint(lambda x, t: odefun(x, t, params_opt), x0, t_sim)
res = solve_ivp(lambda t,x: odefun(t, x, params_opt),[t_sim[0], t_sim[-1]],x0,'RK23', t_eval=t_sim)
x1,x2,x3=res.y
cTnT_sim = sp_interp.interp1d(t_sim, x3)

# Plot the results
plt.plot(time, data, '-', label='Experimental data')
plt.plot(time, cTnT_sim(time), label='Model simulation')
plt.xlabel('Time')
plt.ylabel('Concentration of troponin')
plt.legend()
plt.show()
'''

'''
add = lambda x, y: x + y

print(add(5, 3))  # Prints 8
'''

'''
OBIETTIVI:
1. Sistemare const_func0 e rinominarla: mi deve dare lo stesso numero di MATLAB Obj_troponinModel, cioè 4.8373
Arrays: params, data, time
2.minimize: deve dare gli stessi valori di fmincon_test [-0.8403, -1.7972, 1.8891, -0.3495,  0.6547]
3.basinhopping: risultati devono essere i parametri che vengono usati in best_params di MatLab, 
cioè [0.5941, 0.095959, 70.1804, 7.058, 3.2886]
'''
'''
RISULTATI:
1. Creato nuova funzione obiettivo obj_func, la quale funziona meglio. value=4.820101707026081. Molto vicino a quello di MatLab.
2. Non da tutti gli stessi valori, infatti result.x=[-0.83447486, -2.99989401,  1.47712125, -1.,  0.65471507] che è diversa da fmincon.
3. L'algoritmo basinhopping funziona, ma non da i best_params di MatLab.
'''

