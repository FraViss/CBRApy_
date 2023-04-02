import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

def model(z,t):
    x=z[0]
    y=z[1]
    dxdt=3*np.exp(-t)
    dydt=3-y
    return [dxdt,dydt]

z0=[0,0]
t=np.linspace(0,20,50)
z=odeint(model,z0,t)


plt.plot(t,z)
plt.xlabel('t')
plt.ylabel('z(t)')
plt.show()