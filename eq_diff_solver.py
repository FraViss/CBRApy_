import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

#time
t=np.linspace(0,1,100,endpoint=False)

'''
Il problema è qui. La lunghezza del vettore 't' è n, mentre quella del vettore 'dt' nella
funzione odeint è n-1. Perciò, credo che risolvendo questo "sfasamento" si risolva il
problema.   
'''

#initializing
x=[1,2,3]
v=[1,1,0]

#Variables
Cs_ctnt = x[0]
Cc_ctnt = x[1]
Cp_ctnt = x[2]

#Arguments
a_log = v[0]
b_log = v[1]
Tsc_log = v[2]


# cTnT
Jsc_ctnt = Cs_ctnt - Cc_ctnt
Jcp_ctnt = np.power(10, a_log) * (Cc_ctnt - Cp_ctnt)
Jpm_ctnt = np.power(10, b_log) * Cp_ctnt

#sigmoid curve
G_sc = np.power(t, 3)/ (np.power(t, 3) + np.power(10, (3 * (Tsc_log))))

def odefun(t,x,v): #v=params_log

    #Differential equations
    dCs_ctnt_tau = - Jsc_ctnt * G_sc
    dCc_ctnt_tau = Jsc_ctnt * G_sc - Jcp_ctnt
    dCp_ctnt_tau = Jcp_ctnt

    #Result
    d_concentration = [dCs_ctnt_tau, dCc_ctnt_tau, dCp_ctnt_tau]

    return d_concentration

#initial conditions
x1_0=x[0]
x2_0=x[1]
x3_0=x[2]

#solve
x1=odeint(odefun,x1_0,t,args=(v[0],))
x2=odeint(odefun,x2_0,t,args=(v[1],))
x3=odeint(odefun,x3_0,t,args=(v[2],))

#plot
plt.plot(t,x1,'b',label='x1(t)')
plt.plot(t,x2,'g',label='x2(t)')
plt.plot(t,x3,'r',label='x3(t)')
plt.legend(loc='best')
plt.xlabel('t')
plt.show()