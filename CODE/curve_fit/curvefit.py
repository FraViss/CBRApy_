import numpy as np
from scipy.integrate import solve_ivp
import scipy.interpolate as sp_interp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def model(t, x, params_log):
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
    G_sc = np.power(t, 3) / (np.power(t, 3) + np.power(10, (3 * (Tsc_log))))

    # Differential equations
    dCs_ctnt_tau = - Jsc_ctnt * G_sc
    dCc_ctnt_tau = Jsc_ctnt * G_sc - Jcp_ctnt
    dCp_ctnt_tau = Jcp_ctnt - Jpm_ctnt

    # Result
    return [dCs_ctnt_tau, dCc_ctnt_tau, dCp_ctnt_tau]


def cost_function(t_data, params_log, data):
    # Times at which to store the computed solution, must be sorted and lie within t_span.
    t = np.linspace(0, max(t_data) * 1.6, 201)

    params = np.array([10 ** p for p in params_log])
    # initial parameters
    x0 = [params[-2], params[-1], 0]
    print(x0)
    sol = solve_ivp(model, [0, 300], x0, 'RK23', args=(params,), t_eval=t)
    # get Cp_cTnT
    x1, x2, x3 = sol.y

    cTnT_sim = sp_interp.interp1d(t + params[-1], x3)
    print(cTnT_sim(time))
    # return cost
    print(len(x3))
    print(len(t))
    #plot
    #plt.plot(t,sol[:,0],label='Cs_ctnt')
    #plt.plot(t,sol[:,1],label='Cc_ctnt')
    plt.plot(t,x3,label='Cp_ctnt')
    plt.xlabel('t')
    plt.legend()
    plt.show()
    return np.sum(np.power(data - cTnT_sim(time), 2)*data)

time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]

params = [0.005, 0.005, 30, 0.1, 1]
params_log = np.log10(params)

print(cost_function(time, params_log, data))
