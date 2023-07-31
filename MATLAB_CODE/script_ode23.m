% Dati Acquisizioni
tempo = [5.1333 6.2833 13.1833 29.9167 53.8500 77.2167];
data = [1.43 1.09 0.982 1.22 1.26 0.541];

t_vec_stemi = linspace(0,tempo(end)*1.6,201);

parameter_init = [0.005 0.005 30 0.1 1];
lb = [0.001 0.001 20 0.001 0.1];
ub = [5 5 300 200 400];
% t_vec_stemi=[0 10];
% x0=[7 3 0];

%% Not Optimized plot
params=log10(parameter_init);
disp(params)
x0 = [params(end-1) params(end) 0]';

[T_stemi, X_stemi] = ode23(@(t,x) odefun(t, x, params), t_vec_stemi, x0);
figure(1)
plot(T_stemi,X_stemi(:,3));

%% Optimized plot
best_params = log10([0.5941 0.095959 70.1804 7.058 3.2886]);
disp(best_params)
x0_best = [best_params(end-1) best_params(end) 0]';

[T_stemi, X_stemi] = ode23(@(t,x) odefun(t, x, best_params), t_vec_stemi, x0_best);
figure(2)
plot(T_stemi,X_stemi(:,3));