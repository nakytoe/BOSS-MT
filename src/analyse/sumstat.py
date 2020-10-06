import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

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

def nearest_neighbour(x, sample):
        """
        find point (x') nearest to (x) in set of coordinates (sample),
        calculate distance and return this distance |x-x'|
        """
        diff = lambda a, b: a-b
        limit = lambda a: a if a <= 180 else 360-a
        euc = lambda S: [np.sqrt(sum([limit(d)**2 for d in D])) for D in S]
        dist = np.sort(euc(diff(x, sample)))
        dist = dist[dist != 0] # strip identical points (0 distances)
        return dist[0]

def plot_TL_initialization_strategies(filename, folders):
    """
    Compare TL initialization strategies
    plot:
    - scatter plots of acquisition locations - this is a great way to spot differences
    - histogram of nearest neighbour distances for these plots - to measure coverage and information value
    - potential energy as function of nearest neighbour distance - to measure information value of the points
    """
    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    LARGE_SIZE = 25

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=LARGE_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize

    np.random.seed(123)

    fig, axs = plt.subplots(3,4, figsize = (20,15),
                            sharex = 'row', sharey = 'row',
                        constrained_layout = True)
    titleadd  = ['random uniform', 'sobol', 'BO inorder', 'BO random']
    N = 50 # how many points to include
    # loop through experiments
    for i in range(3):
        folder = folders[i]
        
        dist = []
        exp = folder[0]
        sample = np.array(exp['xy'])[:N,:-1]
        outputs = np.array(exp['xy'])[:N,-1]
        for x, y in zip(sample, outputs):
            dist.append([nearest_neighbour(x, sample), y])
        dist = np.array(dist).reshape(len(sample),2)

        # scatter plot of acuisitions
        ax = axs[0,i]
        titletext = exp['name'].split('_')[0]
        ax.scatter(sample[:,0], sample[:,1], color = 'blue', alpha = 0.5)
        ax.set_title(f'{i+1}a) {titleadd[i]} ({titletext})', loc = 'left')
        ax.set_xlabel('x0')
        ax.set_ylabel('x1')
        
        mean = np.mean(dist[:,0])
        mode = sum(np.sort(dist[:,0])[int(N/2)-1:int(N/2)+1])/2

        # Histogram of nearest neighbour distances
        ax = axs[1,i]
        ax.hist(dist[:,0], color = 'blue', alpha = 0.5)
        ax.axvline(mean, color = 'red', linestyle = 'dashed', label = 'mean', linewidth = 3)
        ax.axvline(mode, color = 'black', linestyle = 'solid', label = 'median', linewidth = 3)
        ax.set_title(f'{i+1}b)', loc = 'left')
        ax.set_xlabel('nearest neighbour distance')
        ax.set_ylabel('count')
        ax.legend()
        
        # potential energy and nearest neighbour distance distance
        ax = axs[2,i]
        ax.scatter(dist[:,0], dist[:,1], color = 'blue', alpha = 0.5)
        ax.set_title(f'{i+1}c)', loc = 'left')
        ax.set_xlabel('nearest neighbour distance')
        ax.set_ylabel('potential energy (kcal/mol)')
        
        
        
        
    for ax in axs.flatten():
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    # BO random sampling - draw samples from BO inorder to simulate how it works
    # (repeat the above for the random sample)
    folder = folders[2]

    dist = []
    exp = folder[0]
    obs = np.array(exp['xy'])
    # bootstrap sample
    #idx = np.random.choice(np.arange(len(obs)), size = N, replace = False)
    idx = np.random.choice(np.arange(len(obs)), size = N, replace = True)
    obs = obs[idx,:]
    sample = np.array(obs)[:N,:-1]
    outputs = np.array(obs)[:N,-1]
    for x, y in zip(sample, outputs):
        dist.append([nearest_neighbour(x, sample), y])
    dist = np.array(dist).reshape(len(sample),2)

    sample = np.unique(sample, axis = 0)
    ax = axs[0,3]
    ax.scatter(sample[:,0], sample[:,1], color = 'blue', alpha = 0.5)
    titletext = exp['name'].split('_')[0]
    ax.set_title(f'4a) {titleadd[3]} ({titletext})', loc = 'left')
    ax.set_xlabel('x0')
    ax.set_ylabel('x1')

    ax = axs[1,3]
    ax.hist(dist[:,0], color = 'blue', alpha = 0.5)
    ax.axvline(mean, color = 'red', linestyle = 'dashed', label = 'mean', linewidth = 3)
    ax.axvline(mode, color = 'black', linestyle = 'solid', label = 'median', linewidth = 3)

    ax.set_title(f'{i+1}b)', loc = 'left')
    ax.set_xlabel('nearest neighbour distance')
    ax.set_ylabel('count')
    ax.legend()
    ax = axs[2,3]
    ax.scatter(dist[:,0], dist[:,1], color = 'blue', alpha = 0.5)
    titletext = exp['name'].split('_')[0]
    ax.set_title(f'4c)', loc = 'left')
    ax.set_xlabel('nearest neighbour distance')
    ax.set_ylabel('potential energy (kcal/mol)')

    plt.savefig(filename)

# Baseline convergence distribution

def baseline_convergence_speed(figname, tablename, baselines, tolerance = 0.1):
    """
    Plot convergence speeds of baselines to given tolerance level
    additionally, test if the convergence speeds differ in BO iterations,
    to measure if the landscape is different in complexity between different simulators
    """
    median = lambda x: np.sort(x)[int(len(x)/2)] if len(x)%2 else np.mean(np.sort(x)[int(len(x)/2):int(len(x)/2)+2])
    N = len(baselines)
    fig, axs = plt.subplots(2,3,figsize = (15, 8), sharey = 'all',
                            constrained_layout = True)
    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    LARGE_SIZE = 30
    convergences = []
    totaltimes = []
    names = []
    for i in range(N):
        convergence_iters = []
        convergence_time = []
        # collect convergence iterations & cpu times
        for exp in baselines[i]:
            j = int(np.where(np.array(exp['tolerance_levels']) == tolerance)[0])
            convergence_iters.append(exp['iterations_to_gmp_convergence'][j])
            convergence_time.append(exp['totaltime_to_gmp_convergence'][j])
        # plot histograms
        for conv, ax in zip([convergence_iters, convergence_time], axs[:,i]):
            ax.hist(conv, color = 'blue', alpha = 0.5)
            # calculate and plot mean and median
            mea = np.mean(conv)
            med = median(conv)
            ax.axvline(mea, color = 'red', linestyle = 'dashed', label = 'mean',
                      linewidth = 3)
            ax.axvline(med, color = 'black', label = 'median', linewidth = 3)
            ax.legend(fontsize = SMALL_SIZE)
        name = baselines[i][0]['name'].split('_')[0]
        names.append(name)
        axs[0,i].set_title(f'{i+1}a) {name}', loc = 'left', fontsize = LARGE_SIZE)
        axs[0,i].set_xlabel('iterations to GMP convergence', fontsize = MEDIUM_SIZE)
        axs[1,i].set_title(f'{i+1}b) {name}', loc = 'left', fontsize = LARGE_SIZE)
        axs[1,i].set_xlabel('CPU time (s) to GMP convergence', fontsize = MEDIUM_SIZE)
        # statistical tests
        convergences.append(convergence_iters)
        totaltimes.append(convergence_time)
            
    for ax in axs.flatten():
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis = 'both',
              width = 3, length = 4, labelsize = SMALL_SIZE)
    plt.savefig(figname)
    # statistical testing to see if the distributions are different
    # how difficult it is to find the minimum in each experiment
    lines = ['task1 & task1 & convergence iterations KS-2S statistic & p-value \\\\']
    for i in range(N):
        for j in range(i+1, N):
            dist_test = ks_2samp(sorted(convergences[i]), sorted(convergences[j]))
            lines.append(f'{names[i]} & {names[j]} & {round(dist_test[0], 2)} & {round(dist_test[1],3)} \\\\')

    with open(tablename, 'w') as f:
        f.writelines(lines)