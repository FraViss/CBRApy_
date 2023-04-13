t_vec_stemi=[0 10];
x0=[1 1 0];
params=[1 1 0];

[T_stemi, X_stemi] = ode23(@(t,x) odefun(t,x,params), t_vec_stemi, x0);
plot(T_stemi,X_stemi(:,3));