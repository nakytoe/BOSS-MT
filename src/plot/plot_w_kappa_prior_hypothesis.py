import sys, io
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

def plot_prior_sumstat_amplitude(filepath):
    ### plot mean and variance for heuristics
    np.random.seed(111)
    fig, axs = plt.subplots(2,4, figsize = (20,10))
    amplitudes = [0.001,0.01,0.1,1,10,100, 1000]
    def sumstat(x):
        return [np.mean(x), np.var(x),ss.skew(x), ss.kurtosis(x, fisher = False)]
    # gamma
    def h0(shape,rate):
        kappa = np.random.gamma(shape, 1/rate, 1000)
        auto = kappa
        cross = None
        return [sumstat(auto), (np.nan, np.nan, np.nan, np.nan)]
    # h1
    def h1(shape, rate):
        w1 = np.random.normal(np.sqrt(shape/rate)*0.9, 1/(shape*np.sqrt(rate)), 1000)
        w2 = np.random.normal(np.sqrt(shape/rate)*0.9, 1/(shape*np.sqrt(rate)), 1000)
        auto = w1**2
        cross = w1*w2
        return [sumstat(auto), sumstat(cross)]
    def h2(shape, rate):
        kappa = np.random.gamma(1, 1/rate, 1000 )
        w1 = (np.random.normal(0, np.sqrt(1/rate), 1000))
        w2 = (np.random.normal(0, np.sqrt(1/rate), 1000))
        auto = w1**2 + kappa
        cross = w1*w2
        return [sumstat(auto), sumstat(cross)]
    def h3(shape,rate):
        w1 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
        w2 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
        w3 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
        w4 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
        auto = w1**2 + w2**2
        cross = w1*w3+w2*w4
        return [sumstat(auto), sumstat(cross)]

    heuristics = [h0,h1,h2,h3]
    names = ['1', '2', '3', '4']
    markers = ['o', 'v', 'x', '+']
    colors = ['red', 'orange','dodgerblue', 'blue']
    first_round = True
    # loop through amplitudes, sample, sumstat and plot
    for A in amplitudes:
        shape = 2
        rate = 2/A**2
        for i in range(4):
            h = heuristics[i]
            values = h(shape, rate)
            auto = list(values[0])
            cross = list(values[1])
            auto[0] = auto[0]
            auto[1] = auto[1]
            cross[0] = cross[0]
            cross[1] = cross[1]
            # label points only once
            if first_round:
                axs[0,0].scatter(A,auto[0], label = names[i],
                            color = colors[i], marker = markers[i])
                axs[0,1].scatter(A,auto[1], label = names[i],
                            color = colors[i], marker = markers[i])
                axs[0,2].scatter(A,auto[2], label = names[i],
                                color = colors[i], marker = markers[i])
                axs[0,3].scatter(A,auto[3], label = names[i],
                            color = colors[i], marker = markers[i])
                # do not plot h0 for second row
                if i != 0:
                    axs[1,0].scatter(A,cross[0], label = names[i],
                                color = colors[i], marker = markers[i])
                    axs[1,1].scatter(A,cross[1], label = names[i],
                                color = colors[i], marker = markers[i])
                    axs[1,2].scatter(A,cross[2], label = names[i],
                                    color = colors[i], marker = markers[i])
                    axs[1,3].scatter(A,cross[3], label = names[i],
                                    color = colors[i], marker = markers[i])
            # plot rest
            else:
                
                axs[0,0].scatter(A,auto[0], 
                            color = colors[i], marker = markers[i])
                axs[0,1].scatter(A,auto[1],
                            color = colors[i], marker = markers[i])
                axs[0,2].scatter(A,auto[2],
                                color = colors[i], marker = markers[i])
                axs[1,0].scatter(A,cross[0], 
                            color = colors[i], marker = markers[i])
                axs[1,1].scatter(A,cross[1], 
                            color = colors[i], marker = markers[i])
                axs[1,2].scatter(A,cross[2],
                                color = colors[i], marker = markers[i])
                axs[0,3].scatter(A,auto[3], 
                            color = colors[i], marker = markers[i])
                axs[1,3].scatter(A,cross[3],
                                color = colors[i], marker = markers[i])
        first_round = False
    # titles
    axs[0,0].set_title('autocovariance prior mean')
    axs[0,1].set_title('autocovariance prior variance')
    axs[1,0].set_title('cross covariance prior mean')
    axs[1,1].set_title('autocovariance prior variance')
    axs[0,2].set_title('autocovariance prior skewness')
    axs[1,2].set_title('cross covariance prior skewness')
    axs[0,3].set_title('autocovariance prior kurtosis')
    axs[1,3].set_title('cross covariance prior kurtosis')
    # plot settings
    for ax, number in zip(axs[0,:], range(1,5)):
        ax.set_title(f'{number}a)', loc = 'left')
        ax.legend(title = 'heuristic', loc = 'upper left')
        ax.set_xscale('log')
        ax.set_yscale('symlog')
        ax.set_xlabel('expected amplitude')
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    for ax, number in zip(axs[1,:], range(1,5)):
        ax.set_title(f'{number}b)', loc = 'left')
        ax.legend(title = 'heuristic', loc = 'upper left')
        ax.set_xscale('log')
        ax.set_yscale('symlog')
        ax.set_xlabel('expected amplitude')
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    axs[0,2].set_yscale('linear')
    axs[1,2].set_yscale('linear')
    axs[0,3].set_yscale('linear')
    axs[1,3].set_yscale('linear')
    # save figure
    plt.savefig(filepath)

def plot_priors_for_1_task(shape,amplitude,filepath):
    """
    plot three alternatives for 1 task autocovariance prior
    """
    # 1 task
    np.random.seed(453)
    fig, axs = plt.subplots(1,3,
                            figsize = (15,5),
                        sharey = 'all', sharex = 'all')
    rate = 2/(amplitude**2)
    # reference Ga(a,b) pdf
   
    gammax = np.linspace(0,500,1000)
    gammay = ss.gamma.pdf(np.linspace(0,500,1000),shape,scale=1/rate)

    # GAMMA
    ax = axs[0]
    variance = np.random.gamma(shape, 1/rate, 1000)
    ax.hist(variance, 30, density = True,
            label = 'kappa', color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 0\nkappa ~Ga(a,b)\nw = 0',
            frameon = False)

    ax = axs[1]
    kappa = np.random.gamma(1, 1/rate, 1000 )
    w = (np.random.normal(0, np.sqrt(1/rate), 1000))
    v = kappa + w**2
    ax.hist(v, 30, density = True, label = 'w^2 + kappa',
        color = 'blue')
    ax.set_title('3)', loc = 'left')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1\nkappa ~Ga(1,b)\nw ~N(0,1/b)',
            frameon = False)
    # NORMAL SQUARED
    ax = axs[2]
    w = (np.random.normal(np.sqrt(shape/rate)*0.9, 1/(shape*np.sqrt(rate)), 1000))**2
    ax.hist(w, 30, density = True, label = 'w^2',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1\nkappa = 0\nw ~N(0.9*sqrt(a/b), 1/(a*sqrt(b)))',
            frameon = False)

    axs[0].set_ylabel('prior pdf')
    for ax, number in zip(axs, range(1,4)):
        ax.set_title(f'{number})', loc = 'left')
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlabel('autocovariance')
    plt.savefig(filepath)

def plot_priors_for_2_tasks(shape,amplitude,filepath):
    np.random.seed(392)
    fig, axs = plt.subplots(2,4,
                        figsize = (20,10),
                     sharey = 'all', sharex = 'all')
    rate = 2/(amplitude**2)
    gammax = np.linspace(0,500,1000)
    gammay = ss.gamma.pdf(np.linspace(0,500,1000),shape,scale=1/rate)

    ## 1
    # RANK 1, kappa ~Ga(a,b), W unpriorized (U(-1,1))

    w1 = ((np.random.rand(1000)-0.5)*2*amplitude)
    w2 = ((np.random.rand(1000)-0.5)*2*amplitude)
    kappa = np.random.gamma(shape, 1/rate, 1000) 
    # 1a) autocovariance
    ax = axs[0,0]
    ax.hist(kappa + w1**2, 30, density = True,
            label = 'w_1^2 + kappa', color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1 \nkappa ~Ga(a,b)\n w ~U(-A,A)',
            frameon = False)
    # 1b) cross covariance
    ax = axs[1,0]
    ax.hist(w1*w2,30, density = True,
            label = 'w_1*w_2', color = 'Blue')
    ## 2
    # RANK 1, kappa ~U(0,1), W ~N(sqrt(a/b),sqrt(a)/b)
    w1 = np.random.normal(np.sqrt(shape/rate)*0.9, 1/(shape*np.sqrt(rate)), 1000)
    w2 = np.random.normal(np.sqrt(shape/rate)*0.9, 1/(shape*np.sqrt(rate)), 1000)
    kappa = np.random.rand(1000)*amplitude**2
    # 2a) autocovariance
    ax = axs[0,1]
    ax.hist(w1**2+kappa, 30, density = True, label = 'w_1^2 + kappa',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title ='W_rank = 1 \nkappa ~U(0,A^2)\n w ~N(0.9*sqrt(a/b),1/(a*sqrt(b)))',
            frameon = False)
    # 2b) cross covariance
    ax = axs[1,1]
    ax.hist(w1*w2, 30, density = True,
            label = 'w_1*w_2',
        color = 'blue')


    ## 3
    # RANK 1, kappa ~Ga(1,1/b), W ~N(0,np.sqrt(1/b))
    kappa = np.random.gamma(1, 1/rate, 1000 )
    w1 = (np.random.normal(0, np.sqrt(1/rate), 1000))
    w2 = (np.random.normal(0, np.sqrt(1/rate), 1000))
    # 3a) autocovariance
    ax = axs[0,2]
    ax.hist(kappa + w1**2, 30, density = True,
            label = 'w_1^2 + kappa',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1 \nkappa ~Ga(1,1/b)\n w ~N(0,1/sqrt(b))',
            frameon = False)
    # 3b) cross covariance
    ax = axs[1,2]
    ax.hist(w1*w2, 30, density = True, label = 'w_1*w_2',
        color = 'blue')

    ## 4) (all instances of a hyperparameter must use same prior in GPy)
    # FULL RANK; kappa 0, W ~N(sqrt(shape/(2*rate)), sqrt(shape)/rate)
    w1 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
    w2 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
    w3 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
    w4 = np.random.normal(np.sqrt(shape/rate/2)*0.9, 1/(shape*np.sqrt(rate)), 1000)
    # autocovariance
    ax = axs[0,3]
    ax.hist(w1**2+w2**2, 30, density = True,
            label = 'w_11^2 + w_12^2',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 2 \nkappa = 0\n w ~N(0.9*sqrt(a/(b*2)),\n 1/(a*sqrt(b)))',
            frameon = False)
    # cross covariance
    ax = axs[1,3]
    ax.hist(w1*w2+w3*w4, 30, density = True,
            label = 'w_11*w_21+w_12*w_22',
        color = 'blue')


    axs[0,0].set_ylabel('prior pdf')
    axs[1,0].set_ylabel('prior pdf')
    for ax, number in zip(axs[0,:], range(1,5)):
        ax.set_title(f'{number}a)', loc = 'left')
        
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlabel('autocovariance')
        
    for ax, number in zip(axs[1,:], range(1,5)):
        ax.set_title(f'{number}b)', loc = 'left')
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.legend(frameon = False)
        ax.set_xlabel('cross covariance')
    plt.savefig(filepath)


if __name__=='__main__':
    """
    get shape, rate and filepaths and 
    make prior plots for 1 and 2 task coregionalization matrix
    """
    args = sys.argv[1:]
    a = int(args[0])
    b = int(args[1])
    filepath_1task = args[2]
    filepath_2task = args[3]
    plot_priors_for_1_task(a,b, filepath_1task)
    plot_priors_for_2_tasks(a,b, filepath_2task)
    filepath_sumstat_amplitude = args[4]
    plot_prior_sumstat_amplitude(filepath_sumstat_amplitude)