import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint
import scipy as sp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from eq_diff_solver import odefun, const_func


#Test
#params = [0.0050, 0.0050, 67.6505, 0.1000, 1.0000]
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina
parameter_init=[0.005, 0.005, 30, 0.1, 1]

print(minimize(const_func, np.log10(parameter_init),args=(data,time)))

