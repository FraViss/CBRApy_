function [T_stemi, X_stemi, params] = troponin_model(data, tempo, function_d, parameter_init, globalfunction, localfunction, number_point, lb, ub)
    
        params_init_log = log10(parameter_init);
    
%% Lower and Upper Bounds
        params_lb_log = log10(lb);
        params_ub_log = log10(ub);

%% Optimization function and data fitting 
%     tic
    func = @(params) function_d(params, data, tempo); %%%%%%%%%%%%%%%%%%%%%Funzione matlab eccetera...

    if (strcmp(globalfunction,'MultiStart')== 1)
%         tic %%%%VVVVVVVVVVVVVVVVVV%%%%
        problem = createOptimProblem (localfunction, ...
               'objective',func,...
               'xdata', tempo,...
               'ydata', data, ...
               'x0', params_init_log,...
               'lb', params_lb_log, ...
               'ub', params_ub_log);
        ms = MultiStart ('MaxTime', 800, 'StartPointsToRun', 'bounds'); %%%%%%%%%%%%%%%%%%%%%%
%         tic
%         assignin("base", "ms", ms);
%         assignin("base", "problem", problem);
%         assignin("base", "number_point", number_point);
        [params,obj_val] = run (ms, problem, number_point); %%%%%%%%%%%%%%%%%%%%%%%%
%         disp(string(toc))
    else
        %parameter_number = length(find(constant_vector == 0));
        parameter_number = 5;
        options = optimoptions('particleswarm','SwarmSize',number_point);
        [params,fval,exitflag,output] = particleswarm(func,parameter_number, params_lb_log,params_ub_log, options); %%%%%%%%%%%%%%%%%%%%%%
    end
    x0 = [params(end-1) params(end) 0]';
    [T_stemi, X_stemi] = ode23(@(t,x) odefun(t,x,params, constant_vector), t_vec_stemi, x0);
end