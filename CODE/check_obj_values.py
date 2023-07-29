import numpy as np
from functions_repository import obj_func

data = [1.4300, 1.0900, 0.9820, 1.2200, 1.2600, 0.5410] #array concentrazione troponina
time = [5.1333, 6.2833, 13.1833, 29.9167, 53.8500, 77.2167] #array tempi di acquisizione troponina
parameter_init=[0.005, 0.005, 30, 0.1, 1]

params_init_log = np.log10(parameter_init)
expected_value= 8.6374 # diverso da 8.63692951000748

def test_check():
    print("Python_obj_value: ",obj_func(params_init_log,data,time))
    print("Matlab_obj_value: ",expected_value)
    assert obj_func(params_init_log,data,time) == expected_value, "Values are not equal"

test_check()
