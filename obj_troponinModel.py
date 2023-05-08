import numpy as np
from scipy.integrate import odeint
import odefun
import scipy as sp
import math
import matplotlib.pyplot as plt

def obj_troponinModel(params, data, time):
    t=np.linspace(0,time[len(time)-1]*1.6,201)
    params=np.power(10,params)
    x0=[params[len(params)-2], params[len(params)-1],0]
    [T,X]=odeint(odefun, y0=x0, t=t, args=(params,))
    cTnT_sim=sp.interpolate.interp1d(T+params[len(params)-1],X[:,2],time)
    obj=np.sum(np.power(data-cTnT_sim,2)*data)

    return obj

def troponin_model(data, time, function_d, parameter_init, globalfunction, localfunction, number_point, lb, ub):
    t_vec_stemi = np.linspace(0,time(len(time)-1)+50,time(len(time-1))+51)
    parameter_init_log = math.log10(parameter_init)
    lb_log = math.log10(lb)
    ub_log = math.log10(ub)

    '''
    func = lambda parameter_init: function_d(parameter_init, data, time)

    if globalfunction == 'MultiStart':
        
    else:
    '''

    x0=[parameter_init[len(parameter_init)-2], parameter_init[len(parameter_init)-1],0]
    [T_stemi,X_stemi]=odeint(odefun,y0=x0,t=t_vec_stemi, args=parameter_init)
    return [T_stemi, X_stemi, parameter_init]

data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina

print(obj_troponinModel([0.005, 0.005, 20, 0.1, 1],data,time))
