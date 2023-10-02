import numpy as np
import scipy.interpolate as sp_interp
from scipy.integrate import odeint,solve_ivp
from scipy.optimize import minimize,optimize
import matplotlib.pyplot as plt
from functions_repository import odefun,cost_function,fmincon_py

#Test
#params = [0.0050, 0.0050, 67.6505, 0.1000, 1.0000]
data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina
parameter_init=[0.005, 0.005, 30, 0.1, 1]

params_init_log = np.log10(parameter_init)

# Bounds
lb = [0.001, 0.001, 20, 0.001, 0.1]  # lower bounds
ub = [5, 5, 300, 200, 400]  # upper bounds
params_lb_log = np.log10(lb)
params_ub_log = np.log10(ub)

def random_point(params_lb_log, params_ub_log):
    return np.random.uniform(params_lb_log, params_ub_log)

def multistart(cost_function, N, params_lb_log, params_ub_log, t_data, data):
    x_star = None
    f_star = np.inf

    success_count = 0

    for i in range(N):
        print(f"\nMultiStart iteration {i + 1} of {N}")  # Check that the loop is running

        x_0 = random_point(params_lb_log, params_ub_log)
        print(f"Initial point: {np.power(10, x_0)}")
        print(f"Lower bounds: {np.power(10, params_lb_log)}")
        print(f"Upper bounds: {np.power(10, params_ub_log)}")

        func = lambda x_0: cost_function(t_data, x_0, data)
        out = fmincon_py(func, params_init_log=x_0, params_lb_log=params_lb_log, params_ub_log=params_ub_log,disp=False)

        print(f"Success: {out['success']}")  # Check that the optimizer is running
        if out["success"]:
            success_count += 1
            print(f"Objective calculated value: {out['fun']}")
            print(f"Optimal parameters: {out['opt_params']}")
            if out["fun"] < f_star:
                x_star = out["opt_params"]
                f_star = out["fun"]

        print(f'Iteration: {i + 1}, Best cost so far: {f_star}, Best params so far: {np.power(10, x_star)}')

    print("\nCompleted MultiStart runs:", success_count, "out of", N)
    print("Minimal cost:", f_star)
    print("Optimal parameters:", np.power(10, x_star))

    return x_star, f_star

# Perform the multistart optimization
params_optimal, minimal_cost = multistart(cost_function, 10, params_lb_log, params_ub_log, time, data)

'''
Ultimi passaggi da fare:

    1. Verificare che nell'esecuzione del MultiStart, ogni punto di partenza ottenuto sia sempre diverso;
    2. Verificare che gli stessi siano sempre all'interno dei boundaries definiti;
    3. Controllare con precisione come il MultiStart di MATLAB sceglie i punti random;
    4. Aggiungere maggiori informazioni in uscita (print per l'utente) nel corso dell'esecuzione 

        (es. per ogni iterazione
            Multistart iteration 3 di N
            Initial point: [ ... ... ]
            Lower bounds: [ ... ... ]
            Upper bounds: [ ... ... ]
            Success: False/True (Se il calcolo ritorna "false", obj_value ed il vettore dei parametri non dovrebbe aggiornarsi per l'iterazione in questione)
            Objective calculated value: ...
            Optimal parameters: [ ... ... ]
        )

        (es. al termine delle N iterazioni
            Completed MultiStart runs: (Numero delle iterazioni completate con successo) out to N
            Objective calculated value: (Il valore migliore ottenuto)
            Optimal parameters: (Migliori parametri associati al valore precedente)
        )

Riepilogo passaggi eseguiti:

    1. La funzione np.random.uniform genera numeri casuali utilizzando un generatore di numeri pseudo-casuali, 
       il che significa che sebbene i numeri sembrino casuali, vengono generati in modo deterministico. 
       Tuttavia, con un buon generatore di numeri pseudo-casuali (come quello utilizzato da NumPy), 
       le possibilità di generare esattamente lo stesso numero due volte sono estremamente ridotte, 
       soprattutto per i numeri in virgola mobile.
       Tuttavia, è importante capire che, in senso puramente matematico, 
       la probabilità di generare ogni volta numeri completamente diversi non è mai del 100%.
       Ciò è dovuto alla natura della casualità e alle infinite possibilità nella gamma dei numeri in virgola mobile.
       Se si sta generando un gran numero di numeri casuali, è teoricamente possibile, 
       anche se estremamente improbabile, che si possa generare lo stesso numero due volte. 
       Ma per scopi pratici, in genere si può presupporre che ogni chiamata a 
       np.random.uniform(params_lb_log, params_ub_log) genererà un numero diverso, 
       purché params_lb_log e params_ub_log definiscano un intervallo che includa più di un numero possibile.
       
    2. La funzione np.random.uniform genera numeri casuali nell'intervallo specificato dai suoi due argomenti, 
       che per impostazione predefinita sono low e high. Nella funzione random_point(params_lb_log, params_ub_log), 
       params_lb_log rappresenta il limite inferiore e params_ub_log rappresenta il limite superiore.
       I numeri generati saranno sempre maggiori o uguali a params_lb_log (il limite inferiore) 
       e minori di params_ub_log (il limite superiore). Si tenga presente che il limite superiore è esclusivo, 
       il che significa che i numeri generati non saranno uguali a params_ub_log, ma sempre strettamente inferiori.
    
    3. MultiStart funziona scegliendo punti di partenza casuali entro i bound constraints del problema. 
       Dopodiché risolve il problema da ciascuno di questi punti iniziali utilizzando un risolutore locale.
       Il metodo specifico utilizzato da MultiStart per scegliere questi punti di partenza non è 
       esplicitamente documentato da MathWorks. 
       Tuttavia, è ragionevole supporre che esso utilizzi una qualche forma di uniform random distribution 
       entro i limiti di ciascuna variabile. Ciò darebbe la migliore possibilità di esplorare a fondo 
       lo spazio del problema e di trovare l’ottimo globale.
       
    4. Ho effettuato delle modifiche al codice e adesso l'esecuzione procede come richiesto e con i print richiesti.
'''