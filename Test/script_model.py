import matplotlib.pyplot as plt
from Test import model_api as api

# Data
# t = np.linspace(0, 10, 100)
# x = np.array([7, 3, 0])
# params_log = np.array([1, 1, 0])
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]
lb = [0.001, 0.001, 20, 0.001, 0.1]
ub = [5, 5, 300, 200, 400]
parameter_init = [0.005, 0.005, 30, 0.1, 1]

# Execution
T_stemi, X_stemi, opt_params = api.troponin_model(data, time, parameter_init, lb, ub)


# Plot results
plt.plot(T_stemi, X_stemi[:, 0], label='Variable 1')
plt.plot(T_stemi, X_stemi[:, 1], label='Variable 2')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()