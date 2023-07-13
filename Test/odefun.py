import numpy as np

def odefun1(t,x,v):
    Cs_ctnt = x[0]
    Cc_ctnt = x[1]
    Cp_ctnt = x[2]
    a_log = v[0]
    b_log = v[1]
    Tsc_log = v[2]


    # cTnT
    Jsc_ctnt = (Cs_ctnt - Cc_ctnt)
    Jcp_ctnt = 10 ** (a_log) * (Cc_ctnt - Cp_ctnt)
    Jpm_ctnt = 10 ** (b_log) * Cp_ctnt

    G_sc = t ** 3 / (t ** 3 + 10 ** (3 * (Tsc_log)))

    dCs_ctnt_tau = - Jsc_ctnt * G_sc
    dCc_ctnt_tau = Jsc_ctnt * G_sc - Jcp_ctnt
    dCp_ctnt_tau = Jcp_ctnt
    d_concentration = [dCs_ctnt_tau, dCc_ctnt_tau, dCp_ctnt_tau]

    return d_concentration


print(odefun(np.arange(0, 5.5, 0.5),[1,2,3,4,5],[1,2,3,4,5]))

#CBRApy