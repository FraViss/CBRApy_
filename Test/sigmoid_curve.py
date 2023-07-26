import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

t=np.linspace(0, 1000, 1000)
Tsc_log=2
G_sc = np.power(t, 3) / (np.power(t, 3) + np.power(10, (3 * (Tsc_log))))

plt.plot(t,G_sc,label='G_sc')
plt.legend()
plt.xlabel('t')
plt.grid()
plt.show()