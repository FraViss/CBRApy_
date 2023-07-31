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
    cTnT_sim = sp_interp.interp1d(t_vec+params[-1],bounds_error=False, fill_value="extrapolate")(time)
    obj = np.sum(((data - cTnT_sim) ** 2) * data)
    return obj
'''
#FUNZIONE OBIETTIVO DEFINITIVA!
def cost_function(t_data, params_log, data):
    t = np.linspace(0, max(t_data) * 1.6, 201)
    #params = np.array([10 ** p for p in params_log])
    x0 = [10**(params_log[-2]), 10**(params_log[-1]), 0]
    sol = solve_ivp(odefun, [t[0], t[-1]], x0, 'RK23', args=(params_log,), t_eval=t)
    x1, x2, x3 = sol.y
    cTnT_sim = sp_interp.interp1d(t + params_log[-1], x3,bounds_error=False,fill_value="extrapolate")
    return np.sum(np.power(data - cTnT_sim(t_data), 2)*data)
'''
def obj_func(params_init_log, data, time):
    #params = 10 ** parameter_init
    params = np.array(np.power(10, params_init_log))
    x0 = np.array([params[-2], params[-1], 0])
    t_vec = np.linspace(0, time[-1] * 1.6, 201)
    res = odeint(lambda x,t: odefun(t, x, params), x0, t_vec)
    x1, x2, x3 = res.T
    cTnT_sim= sp_interp.interp1d(t_vec+params[-1], x3, bounds_error=False, fill_value="extrapolate")(time)
    obj = np.sum(((data - cTnT_sim) ** 2) * data)
    return obj
'''

if __name__=="__main__":
    data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]  # array concentrazione troponina
    time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]  # array tempi di acquisizione troponina
    parameter_init = [0.005, 0.005, 30, 0.1, 1]
    params = np.log10(parameter_init)

    t_vec_stemi= np.linspace(0, max(time)*1.6, 201)

    #print(cost_function(time,params,data))

    print("Test odefun non optimized.")
    print("parameter_init: ",parameter_init)
    print("log10_parameter_init: ",params)
    x0=[10**(params[-2]),10**(params[-1]),0]
    sol = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params,), t_eval=t_vec_stemi)
    x1, x2, x3 = sol.y
    #Plot test
    plt.figure()
    plt.plot(t_vec_stemi, x3, label='Not')
    plt.title("Non-Optimized")
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()

    print("Test local odefun optimized")
    fmincon_params = [0.4676, 0.1120, 70.2712, 8.1746, 3.4479]
    print("best_params: ", fmincon_params)
    params_log = np.log10(fmincon_params)
    print("log10: ",params_log)
    x0 = [10**(params_log[-2]), 10**(params_log[-1]), 0]
    sol1 = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params_log,), t_eval=t_vec_stemi)
    x_1, x_2, x_3 = sol1.y
    # Plot test
    plt.figure()
    plt.plot(t_vec_stemi, x_3, label='Local')
    plt.title("Local Optimized")
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()

    print("Test SLSQP")
    best_params_slsqp =[0.68414505, 0.1110646, 71.28444528, 8.05371601, 3.42948988]
    print("best_params: ", best_params_slsqp)
    params_log = np.log10(best_params_slsqp)
    print("log10: ",params_log)
    x0 = [10**params_log[-2], 10**params_log[-1], 0]
    t_vec_stemi = np.linspace(0, max(time) * 1.6, 201)
    sol1 = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params_log,), t_eval=t_vec_stemi)
    x_1, x_2, x_3 = sol1.y
    # Plot test
    plt.figure()
    plt.plot(t_vec_stemi, x_3, label='Locally py optim')
    plt.title("Local SLSQP optimized")
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()

    print("Test odefun optimized")
    best_params =[0.5941, 0.095959, 70.1804, 7.058, 3.2886]
    print("best_params: ",best_params)
    params_log = np.log10(best_params)
    print("log10: ",params_log)
    x0 = [10**params_log[-2], 10**params_log[-1], 0]
    t_vec_stemi = np.linspace(0, max(time) * 1.6, 201)
    sol1 = solve_ivp(odefun, [t_vec_stemi[0], t_vec_stemi[-1]], x0, 'RK23', args=(params_log,), t_eval=t_vec_stemi)
    x_1, x_2, x_3 = sol1.y
    # Plot test
    plt.figure()
    plt.plot(t_vec_stemi, x_3, label='Optimized')
    plt.title("Optimized")
    plt.xlabel('Time')
    plt.ylabel('Concentration of troponin')
    plt.legend()
    plt.show()



'''
fmincon ->  [0.4676, 0.1120, 70.2712, 8.1746, 3.4479] test: 0.0583

Powell -> params: [6.52486132e-01 1.83710494e-03 2.06583851e+02 4.62499485e-03 2.47327792e+00] test: 0.23895693256668382
L-BFGS-B -> [-2.30243659 -2.30896236  1.47712125 -0.99999992  0.65471223] test: 4.873334848794853
TNC -> [-2.3026514  -2.30939459  1.47712125 -1.00000032  0.65471223] test: 4.873328909516684
COBYLA -> [3.69114515e-01 6.88285997e-03 6.21154100e+02 9.81958959e-01 2.55364526e+00] test: 0.3004244146956698
SLSQP -> [0.68414505  0.1110646  71.28444528  8.05371601  3.42948988] test: 0.050021961014945784
trust-constr -> [-2.14567736 -2.16467664  1.76293427 -0.92086449  0.65471223] test: 4.874830122298463

'''