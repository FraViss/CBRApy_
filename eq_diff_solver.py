import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint


def odefun(x,t,params_log):

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
t=np.linspace(0,10,100)
x0=np.array([7,3,0])
params_log=[1,1,0]


#solve
sol=odeint(odefun, y0=x0, t=t, args=(params_log,))

#plot
#plt.plot(t,sol[:,0],label='Cs_ctnt')
#plt.plot(t,sol[:,1],label='Cc_ctnt')
plt.plot(t,sol[:,2],label='Cp_ctnt')
plt.xlabel('t')
plt.legend()
plt.show()


#x=7,3,0
#params_log=-0.23,-1.02,1.85
