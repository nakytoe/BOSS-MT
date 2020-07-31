import numpy as np


def get_exp_namebases(folders):
    """
    get list of experiment folders
    return list of folder namebases
    """
    ret = []
    for folder in folders:
        name = folder[0]['name'].split('_')[0]
        ret.append(name)
    return ret

def calc_fx_sumstat(folder):
    """
    return N_exp, f(x): mean var min max amplitude
    """
    N_exp = len(folder)
    ret = [N_exp]
    fxlist = []
    for exp in folder:
        fx = np.array(exp['xy'])[:,-1]
        fxlist.append(fx)
    fxlist = np.array(fxlist).flatten()
    # obs mean
    ret.append(np.mean(fxlist))
    # var
    ret.append(np.var(fxlist))
    # min
    ret.append(min(fxlist))
    # max
    ret.append(max(fxlist))
    # amplitude
    A = (max(fxlist)-min(fxlist))/2
    ret.append(A)
    # rate parameter for variance prior
    rate = 2/(A**2)
    ret.append(rate)
    return ret

def summarize_folders_fx(folders):
    """
    summary statistics for a list of experiments

    name, N_exp, f(x): mean var min max amplitude
    """
    N_f = len(folders)
    colnames = get_exp_namebases(folders)
    rownames = ['exp','$N_{exp}$', '$m(\f{\vx})$',
     '$var(\f{\vx})$', '$min(\f{\vx})$', '$max(\f{\vx})$', '$A(\f{\vx})$',
     '\sigma^2 prior rate' ]
    ret = []
    for folder in folders:
        sumstat = calc_fx_sumstat(folder)
        ret.append(sumstat)
    return ret, colnames, rownames