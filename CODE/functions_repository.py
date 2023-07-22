import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.interpolate as sp_interp
from scipy.integrate import odeint
import scipy.stats as ss

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
def const_func0(parameter_init, data, time):
    params = 10 ** parameter_init
    x0 = [params[-2], params[-1], 0]
    t_vec = np.linspace(0, time[-1] * 1.6, 201)
    X = odeint(lambda x, t: odefun(x, t, params), x0, t_vec)
    cTnT_sim = sp_interp.interp1d(t_vec, X[:, 2])(time)
    obj = np.sum(((data - cTnT_sim) ** 2) * data)
    return obj

def const_func(params, data, time):
    t = np.linspace(0, max(time) * 1.6, 201)
    params = np.array([10 ** p for p in params])
    x0 = np.array([params[-2], params[-1], 0])
    x = odeint(odefun, x0, t, args=(params,))

    unique_x = np.unique(t + params[-1])
    unique_t = np.unique(t)  # Add this line to obtain unique t values

    # Interpolate using unique_t as the x-coordinates and x[:, 2] as the y-coordinates
    cTnT_sim = sp_interp.interp1d(unique_x, x[:, 2], kind='cubic', bounds_error=False)

    # Evaluate the interpolated function at the desired time points
    cTnT_sim_vals = cTnT_sim(unique_t)

    # Interpolate the simulated values at the actual time points
    interpolated_vals = sp_interp.interp1d(unique_t, cTnT_sim_vals, kind='cubic', bounds_error=False)

    obj = np.sum(np.power(data - interpolated_vals(time), 2) * data)
    return obj




def const_func1(params, data, time):
    t = np.linspace(0, max(time) * 1.6, 201)
    params = np.array([10 ** p for p in params])
    x0 = np.array([params[-2], params[-1], 0])
    x = odeint(odefun, x0, t, args=(params,))
    cTnT_sim = sp_interp.interp1d(t + params[-1], x[:, 2], kind='cubic',bounds_error=False) # approfondire interp1d # test linear e quadratic
    obj = np.sum(np.power(data - cTnT_sim(time), 2)*data) # questa operazione va rivista aggiungere moltiplicazione per data
    return obj
'''
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
'''