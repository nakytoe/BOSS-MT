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
    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    LARGE_SIZE = 30

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=LARGE_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=LARGE_SIZE)  # fontsize of the figure title
    fig, axs = plt.subplots(N,N,
                figsize = (N*5,N*5),
                       constrained_layout = True)
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
            ax.set_xticks(axs[0,1].get_yticks())
            ax.set_yticks(axs[0,1].get_xticks())
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.tick_params(axis = 'both',
              width = 3, length = 4)
        # remove below-diagonal plots
        for j in range(i):
            ax = axs[i,j]
            ax.axis('off')
        
    
    axs[0,N-1].set_xticklabels([])
    axs[0,N-1].set_yticklabels([])    

    plt.savefig(figname)

def timings_plot_table(figname, folders):
    """
    Plot mean acquisition times for different simulators based on sobol experiments
    return table of timing ratios
    """
    font = {'size'   : 22}
    plt.rc('font', **font)

    fig, axs = plt.subplots(1, figsize = (5,5),
                    constrained_layout = True)
    names = ['LF', 'HF', 'VHF']
    ax = axs

    ax.tick_params(axis = 'both',
                length = 0)
    ### plot mean acquisition times
    ratios = []
    for i in range(3):
        exp = folders[i][0]
        acq_mean = np.mean(exp['acqtime'])
        ax.bar(i,  acq_mean, color = 'blue')
        ax.annotate(f'{round(acq_mean, 2)}', [i-0.3,acq_mean+1])
        ratio = []
        for j in range(3):
            ratio.append(acq_mean/np.mean(folders[j][0]['acqtime']))
        ratios.append(ratio)
    for tick in ax.get_yticks()[1:-1]:
        ax.axhline(tick, color = 'white', linewidth = 5)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticks(range(3))
    ax.set_xticklabels(names)
    ax.set_xlabel('simulation fidelity')
    ax.set_ylabel('mean acq. time [s]')

    plt.savefig(figname)

    ## print acquisition time ratios to table
    lines = []
    line = ''
    for fidelity in names:
        line = f'{line} & {fidelity}'
    line = f'{line} \\\\'
    lines.append(line)
    for i in range(3):
        line = f'{names[i]}'
        for ratio in ratios[i]:
            line = f'{line} & {round(ratio, 2)}'
        line = f'{line} \\\\'
        lines.append(line)

    return lines