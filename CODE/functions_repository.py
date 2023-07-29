import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt


def odefun(t,x,params_log):

    # Variables
    Cs_ctnt = x[0]
    Cc_ctnt = x[1]
    Cp_ctnt = x[2]

    # Arguments
    a_log = params_log[0]
    b_log = params_log[1]
    Tsc_log = params_log[2]

    # cTnT
    Jsc_ctnt = Cs_ctnt - Cc_ctnt
    Jcp_ctnt = np.power(10, a_log) * (Cc_ctnt - Cp_ctnt)
    Jpm_ctnt = np.power(10, b_log) * Cp_ctnt

    # sigmoid curve
    G_sc = np.power(t, 3) / (np.power(t, 3) + np.power(10, (3 * Tsc_log)))

    #Differential equations
    dCs_ctnt_tau = - Jsc_ctnt * G_sc
    dCc_ctnt_tau = Jsc_ctnt * G_sc - Jcp_ctnt
    dCp_ctnt_tau = Jcp_ctnt - Jpm_ctnt

    #Result
    d_concentration = [dCs_ctnt_tau, dCc_ctnt_tau, dCp_ctnt_tau]

    return d_concentration
'''
def objective_func(params_init_log, data, time):
    #params = 10 ** parameter_init
    params = np.array(np.power(10, params_init_log))
    x0 = np.array([params[-2], params[-1], 0])
    t_vec = np.linspace(0, time[-1] * 1.6, 201)
    res = solve_ivp(lambda t, x: odefun(t, x, params),[t_vec[0], t_vec[-1]], x0, 'RK23', t_eval=t_vec)
    x1, x2, x3 = res.y
    cTnT_sim = sp_interp.interp1d(t_vec, x3)(time)
    obj = np.sum(((data - cTnT_sim) ** 2) * data)
    return obj
'''

#FUNZIONE OBIETTIVO MIGLIORE!
def obj_func(params_init_log, data, time):
    #params = 10 ** parameter_init
    params = np.array(np.power(10, params_init_log))
    x0 = np.array([params[-2], params[-1], 0])
    t_vec = np.linspace(0, time[-1] * 1.6, 201)
    res = odeint(lambda x,t: odefun(t, x, params), x0, t_vec)
    x1, x2, x3 = res.T
    cTnT_sim = sp_interp.interp1d(t_vec+params[-1], x3, bounds_error=False, fill_value="extrapolate")(time)
    obj = np.sum(((data - cTnT_sim) ** 2) * data)
    return obj


if __name__=="__main__":
    print("Test odefun non optimized.")
    data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]  # array concentrazione troponina
    time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]  # array tempi di acquisizione troponina
    parameter_init = [0.005, 0.005, 30, 0.1, 1]
    print("parameter_init: ",parameter_init)
    params=np.log10(parameter_init)
    print("log10_parameter_init: ",params)
    x0=[params[-2],params[-1],0]
    t_vec_stemi= np.linspace(0, max(time)*1.6, 201)
    sol = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params,), t_eval=t_vec_stemi)
    x1, x2, x3 = sol.y
    #Plot test
    plt.figure()
    plt.plot(t_vec_stemi, x3, label='Sol')
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()

    print("Test odefun optimized")
    #best_params =[0.5941, 0.095959, 70.1804, 7.058, 3.2886]
    best_params=[-3. ,        -3.,          1.52613105 ,-0.71888118,  1.38195932]
    best_params=np.power(10,best_params)
    print("best_params: ",best_params)
    params_log = np.log10(best_params)
    print("log10: ",params_log)
    x0 = [params_log[-2], params_log[-1], 0]
    t_vec_stemi = np.linspace(0, max(time) * 1.6, 201)
    sol1 = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params_log,), t_eval=t_vec_stemi)
    x_1, x_2, x_3 = sol1.y
    # Plot test
    plt.figure()
    plt.plot(t_vec_stemi, x_3, label='Sol1')
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()
    '''
    X = odeint(lambda x, t: odefun(t,x, params_log), x0, t_vec_stemi)
    plt.plot(t_vec_stemi, X[:,2], label='Test plot')
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()
    '''
    #sol1 = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params_log,), t_eval=t_vec_stemi)
    #x_1, x_2, x_3 = sol1.y
    X = solve_ivp(lambda t,x: odefun(t, x, params_log), [t_vec_stemi[0], t_vec_stemi[-1]],x0,'RK23', t_eval=t_vec_stemi)
    x1_,x2_,x3_=X.y
    plt.figure()
    plt.plot(t_vec_stemi, x3, label='X')
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()
