 function d_concentration = odefun(t, x, params_log)

%  cTnT
    Cs_ctnt = x(1);      % concentration of cTnT into sarcomere
    Cc_ctnt = x(2);      % concentration of cTnT into cytosol
    Cp_ctnt = x(3);      % concentration of cTnT into plasma

    a_log = params_log(1);
    b_log = params_log(2); 
    Tsc_log = params_log(3);

    Jsc_ctnt = (Cs_ctnt - Cc_ctnt);
    Jcp_ctnt = 10^(a_log)*(Cc_ctnt - Cp_ctnt);
    Jpm_ctnt = 10^(b_log)*Cp_ctnt;

    G_sc = t^3/(t^3 + 10^(3*(Tsc_log)));
    dCs_ctnt_tau = - Jsc_ctnt*G_sc;
    dCc_ctnt_tau =   Jsc_ctnt*G_sc - Jcp_ctnt;
    dCp_ctnt_tau =   Jcp_ctnt - Jpm_ctnt;
    d_concentration = [dCs_ctnt_tau; dCc_ctnt_tau; dCp_ctnt_tau];

end