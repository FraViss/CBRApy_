import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

def odefun(t,x,v): #v=params_log
    Cs_ctnt = x[0]
    Cc_ctnt = x[1]
    Cp_ctnt = x[2]
    a_log = v[0]
    b_log = v[1]
    Tsc_log = v[2]


    # cTnT
    Jsc_ctnt = (Cs_ctnt - Cc_ctnt)
    Jcp_ctnt = np.power(10, a_log) * (Cc_ctnt - Cp_ctnt)
    Jpm_ctnt = np.power(10, b_log) * Cp_ctnt

    G_sc = np.power(t, 3)/ (np.power(t, 3) + np.power(10, (3 * (Tsc_log))))

    dCs_ctnt_tau = - Jsc_ctnt * G_sc
    dCc_ctnt_tau = Jsc_ctnt * G_sc - Jcp_ctnt
    dCp_ctnt_tau = Jcp_ctnt
    d_concentration = [dCs_ctnt_tau, dCc_ctnt_tau, dCp_ctnt_tau]

    return d_concentration
#time
t=np.linspace(0,1,100)

#initial conditions
x0=[1,1,0]

#solve
x=odeint(odefun,x0,t,args=(1,2,3))

#plot
plt.plot(t,x)
plt.legend('x(t)')
plt.xlabel('t')
plt.show()