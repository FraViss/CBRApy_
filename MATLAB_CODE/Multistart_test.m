data = [1.4300 1.0900 0.9820 1.2200 1.2600 0.5410]; %array concentrazione troponina
tempo =[5.1333 6.2833 13.1833 29.9167 53.8500 77.2167]; %array tempi di acquisizione troponina
parameter_init = [0.005 0.005 30 0.1 1];

lb = [0.001 0.001 20 0.001 0.1]; %lower bounds
ub = [5 5 300 200 400]; %upper bounds

localfunction = 'fmincon';
globalfunction = 'MultiStart';
number_point = 40;

[T_stemi, X_stemi, params] = troponin_model(data, tempo, @Obj_TroponinModel, parameter_init, globalfunction, localfunction, number_point, lb, ub);

disp(10.^params)