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
t=np.linspace(0,10,100)
x0=np.array([7,3,0])
params_log=[1,1,0]


#solve
# sol=odeint(odefun, y0=x0, t=t, args=(params_log,))
sol = solve_ivp(odefun, [0, 201], x0, 'RK23', args=(params_log,), t_eval=t)
x1, x2, x3 = sol.y
print(len(x3))
print(len(t))
#plot
#plt.plot(t,sol[:,0],label='Cs_ctnt')
#plt.plot(t,sol[:,1],label='Cc_ctnt')
plt.plot(t,x3,label='Cp_ctnt')
plt.xlabel('t')
plt.legend()
plt.show()


#x=7,3,0
#params_log=-0.23,-1.02,1.85
