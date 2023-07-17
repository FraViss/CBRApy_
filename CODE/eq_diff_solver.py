import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint, solve_ivp


def odefun(t, x, params_log):

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

#initial conditions
# t=np.linspace(0,10,100)
# time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167]
# data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410]

# params = [0.005, 0.005, 30, 0.1, 1]
# params_log = np.log10(params)

# params = np.array([10 ** p for p in params_log])

# x0 = [params[-2], params[-1], 0]

# t = np.linspace(0, max(time) * 1.6, 201)
# x0=np.array([7,3,0])
# params_log=[1,1,0]


# #solve
# # sol=odeint(odefun, y0=x0, t=t, args=(params_log,))
# print(t[0])
# print(t[-1])
# sol = solve_ivp(odefun, [t[0], t[-1]], x0, 'RK23', args=(params,), t_eval=t)
# x1, x2, x3 = sol.y
# print(len(x3))
# print(len(t))
# #plot
#plt.plot(t,sol[:,0],label='Cs_ctnt')
#plt.plot(t,sol[:,1],label='Cc_ctnt')
# plt.plot(t,x3,label='Cp_ctnt')
# plt.xlabel('t')
# plt.legend()
# plt.show()


#x=7,3,0
#params_log=-0.23,-1.02,1.85
