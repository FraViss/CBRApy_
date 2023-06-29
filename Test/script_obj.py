data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina
lb = [0.001, 0.001, 20, 0.001, 0.1] #lower bound
ub = [5, 5, 300, 200, 400] #upper bound
globalfunction = 'MultiStart' # oppure 'particleswarm'
localfunction = 'fmincon'
parameter_init = [0.005, 0.005, 30, 0.1, 1] # parametri iniziali
number_point = 1 # %40 %25 1