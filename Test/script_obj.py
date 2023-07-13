import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint

params = [0.0050, 0.0050, 67.6505, 0.1000, 1.0000]
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina

'''
lb = [0.001, 0.001, 20, 0.001, 0.1] #lower bound
ub = [5, 5, 300, 200, 400] #upper bound
globalfunction = 'MultiStart' # oppure 'particleswarm'
localfunction = 'fmincon'
parameter_init = [0.005, 0.005, 30, 0.1, 1] # parametri iniziali
number_point = 1 # %40 %25 # 1
'''

def const_func(params, data, time):
    t = np.linspace(0, max(time) * 1.6, 201)
    params_log = np.array([10 ** p for p in params])
    x0 = np.array([params_log[-2], params_log[-1], 0])
    x = odeint(odefun, x0, t, args=(params_log,))
    cTnT_sim = sp_interp.interp1d(t + params_log[-1], x[:, 2], kind='cubic',bounds_error=False) # approfondire interp1d # test linear e quadratic
    obj = np.sum(np.power(data - cTnT_sim(time), 2)*data) # questa operazione va rivista aggiungere moltiplicazione per data
    return obj

print(const_func(np.log10(params),data,time))
