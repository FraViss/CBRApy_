import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, basinhopping
import eq_diff_solver as odefun
import scipy as sp
from pyomo.environ import *

def obj_troponinModel(params, data, time):
    t = np.linspace(0, max(time)*1.6, 201)
    params = np.power(10, params)
    x0 = [params[-2], params[-1], 0]
    X = odeint(odefun, x0, t, args=(params,))
    cTnT_sim = sp.interpolate.interp1d(t+params[-1], X[:,2], time)
    obj = np.sum(np.power(data-cTnT_sim(time), 2)*data)
    return obj

def troponin_model(data, tempo, function_d, parameter_init, globalfunction, localfunction, number_point, lb, ub):
    #function_d è obj_troponinModel: la funzione obiettivo.
    t_vec_stemi = np.linspace(0, int(max(tempo)+50), int(max(tempo)+51))
    params_init_log = np.log10(parameter_init)
    params_lb_log = np.log10(lb)
    params_ub_log = np.log10(ub)
    if globalfunction == 'MultiStart':
        problem = {'func': obj_troponinModel,
                   'args': (data, tempo),
                   'x0': params_init_log,
                   'bounds': list(zip(params_lb_log, params_ub_log)),
                   'method': localfunction
                   }
        ms = basinhopping(**problem, niter=number_point)
        params = ms.x
    else:
        parameter_number = 5
        options = {'swarm_size': number_point}
        res = minimize(obj_troponinModel, params_init_log, args=(data, tempo),
                       method='powell', bounds=list(zip(params_lb_log, params_ub_log)), options=options)
        params = res.x
    x0 = [params[-2], params[-1], 0]
    print('Solving model')
    T_stemi, X_stemi = odeint(odefun, x0, t_vec_stemi, args=(params,))
    return [T_stemi, X_stemi, params]
