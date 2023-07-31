function obj = Obj_TroponinModel(params, data, time_pat)
% =========================================================================
%  Cost function. This function receives as input:
%         params: estimated parameters
%         ctnt: experimental cTnT data;
%         ckmb: experimental CK-MB data;   
%         time_pat: acquisition time;
% =========================================================================
    t_vec = linspace(0,time_pat(end)*1.6,201);
    % params = 10.^(params);
    x0 = [10^(params(end-1)) 10^(params(end)) 0]';
    [T, X] = ode23(@(t,x) odefun(t,x,params), t_vec, x0);
    cTnT_sim = interp1(T + params(end), X(:,3),time_pat);
    obj = sum(((data - cTnT_sim).^2).*data);
end
