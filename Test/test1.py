import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize

# Definisci il sistema ODE
def my_system(y, t, params):
    # Definisci le equazioni differenziali del sistema
    # y: vettore delle variabili di stato
    # t: tempo
    # params: vettore dei parametri del sistema
    # Restituisci le derivate delle variabili di stato
    # in base alle equazioni differenziali del sistema
    dydt = np.zeros_like(y)
    dydt[0] = params[0] * y[0] + params[1] * y[1]
    dydt[1] = params[2] * y[0] + params[3] * y[1]
    return dydt

# Definisci la funzione obiettivo da minimizzare
def objective(params):
    # Definisci le condizioni iniziali e il tempo
    y0 = [1.0, 2.0]  # Condizioni iniziali
    t = np.linspace(0, 10, 100)  # Tempo

    # Risolvi il sistema ODE con le condizioni iniziali e i parametri correnti
    y = odeint(my_system, y0, t, args=(params,))

    # Calcola la differenza tra i risultati del sistema ODE e i dati osservati
    # (qui puoi inserire la tua logica specifica)
    # Ad esempio, calcola l'errore quadratico medio tra y[:, 0] e i dati osservati
    observed_data = np.array([1.5, 3.0, 4.5, 6.0, 7.5])  # Dati osservati
    predicted_data = y[:, 0]  # Dati predetti dal sistema ODE
    error = np.mean((predicted_data - observed_data) ** 2)

    return error

# Definisci i valori iniziali dei parametri per l'ottimizzazione
initial_params = [0.1, 0.2, 0.3, 0.4]

# Esegui l'ottimizzazione locale utilizzando la funzione minimize
result = minimize(objective, initial_params, method='BFGS')

# Stampa i risultati dell'ottimizzazione
print(result)
print("Parametri ottimizzati:", result.x)
print("Valore minimo della funzione obiettivo:", result.fun)
