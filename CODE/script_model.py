import numpy as np
import matplotlib.pyplot as plt
import model_api as api
from scipy.optimize import minimize, rosen


# Data
# t = np.linspace(0, 10, 100)
# x = np.array([7, 3, 0])
# params_log = np.array([1, 1, 0])
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]
lb = [0.001, 0.001, 20, 0.001, 0.1]
ub = [5, 5, 300, 200, 400]
parameter_init = [0.005, 0.005, 30, 0.1, 1]

# print(api.obj_troponinModel(params_log, data, time))

# Execution
result = minimize(api.obj_troponinModel, parameter_init, method='BFGS', args=(data, time))

print(result)
print("Parametri ottimizzati:", result.x)
print("Valore minimo della funzione obiettivo:", result.fun)

