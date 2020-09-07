import numpy as np
import matplotlib.pyplot as plt

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

def calculate_covariance(explist):
    """
    calculate covariance matrix for a structure
    params;
    explist: list of equally queried sobol experiments from different simulators
    return;
    covariance matrix
    """
    N = len(explist)
    covariance_matrix = np.zeros((N,N), dtype = float)
    for i in range(N):
        # read observations
        y1 = np.array(explist[i]['xy'])[:,-1]
        # center
        y1 = y1-np.mean(y1)
        for j in range(N):
            y2 = np.array(explist[j]['xy'])[:,-1]
            y2 = y2-np.mean(y2)
            covariance_matrix[i,j] = np.cov(np.hstack((y1,y2)), rowvar=False)
    return covariance_matrix

def calculate_correlation(explist):
    """
    calculate correlation matrix for a structure
    params;
    explist: list of equally queried sobol experiments from different simulators
    return;
    correlation matrix
    """
    N = len(explist)
    corr_matrix = np.zeros((N,N), dtype = float)
    for i in range(N):
        # read observations
        y1 = np.array(explist[i]['xy'])[:,-1]
        # center
        y1 = y1-np.mean(y1)
        for j in range(N):
            y2 = np.array(explist[j]['xy'])[:,-1]
            y2 = y2-np.mean(y2)
            corr_matrix[i,j] = np.corrcoef(y1,y2, rowvar= False)[0,1]
    return corr_matrix

def plot_y_scatter_trellis(explist, figname):
    # plot scatter plot trellis of sobol queue experiment y observations
    N = len(explist)
    fig, axs = plt.subplots(N,N,
                figsize = (N*5,N*5))
    for i in range(N):
        # plot name of the experiment as axis label
        ax = axs[i,i]
        ax.axis('off')
        exp1 = explist[i]
        name = exp1['name'].split('_')[0]
        ax.text(0.5, 0.5, f'{name} (kcal/mol)',
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=30,
            transform=ax.transAxes)
        # make scatter plots of y values
        for j in range(i+1, N):
            ax = axs[i,j]
            exp1 = explist[j]
            exp2 = explist[i]
            x = np.array(exp1['xy'])[:,-1]
            y = np.array(exp2['xy'])[:,-1]
            ax.scatter(x,y, marker = 'x',
                    color = 'blue',
                    alpha = 0.5)
            ax.set_xticks(ax.get_yticks())
            ax.set_yticks(ax.get_xticks())
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
        # remove below-diagonal plots
        for j in range(i):
            ax = axs[i,j]
            ax.axis('off')
    
    axs[0,N-1].set_xticklabels([])
    axs[0,N-1].set_yticklabels([])    

    plt.savefig(figname)