import sys, io
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

def plot_priors_for_1_task(a,b,filepath):
    """
    plot three alternatives for 1 task autocovariance prior
    """
    fig, axs = plt.subplots(1,3,
                            figsize = (15,5),
                        sharey = 'all', sharex = 'all')
    shape = a
    rate = b
    # reference Ga(a,b) pdf
    gammax = np.linspace(0,1,100)
    gammay = ss.gamma.pdf(np.linspace(0,1,100),shape,scale=1/rate)
   
    ## 1)
    # Rank 0, kappa ~Ga(a,b), w = 0
    ax = axs[0]
    variance = np.random.gamma(shape, 1/rate, 1000)
    ax.hist(variance, 30, density = True,
            label = 'kappa', color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 0\nkappa ~Ga(a,b)\nw = 0',
            frameon = False)
    

    ## 2)
    # rank 1, kappa ~Ga(1,b), w ~N(0,1/b)
    ax = axs[1]
    kappa = np.random.gamma(1, 1/rate, 1000 )
    w = np.random.normal(0, np.sqrt(1/rate), 1000)
    ax.hist(w**2 + kappa, 30, density = True, label = 'w^2 + kappa',
        color = 'blue')
    ax.set_title('3)', loc = 'left')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1\nkappa ~Ga(1,b)\nw ~N(0,1/b)',
            frameon = False)
    ## 3)
    # rank = 1, kappa = 0, w ~N(sqrt(a/b), sqrt(2)/b)
    ax = axs[2]
    w = (np.random.normal(np.sqrt(shape/rate), np.sqrt(shape)/rate, 1000))**2
  
    ax.hist(w, 30, density = True, label = 'w^2',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1\nkappa = 0\nw ~N(sqrt(a/b), sqrt(2)/b)',
            frameon = False)

    axs[0].set_ylabel('prior pdf')
    for ax, number in zip(axs, range(1,4)):
        ax.set_title(f'{number})', loc = 'left')
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlabel('autocovariance')
    # save figure
    plt.savefig(filepath)

def plot_priors_for_2_tasks(a,b,filepath):
    fig, axs = plt.subplots(2,4,
                        figsize = (20,10),
                       sharey = 'all', sharex = 'all')
    shape = a
    rate = b
    gammax = np.linspace(0,1,100)
    gammay = ss.gamma.pdf(np.linspace(0,1,100),shape,scale=1/rate)
   
    ## 1
    # RANK 1, kappa ~Ga(a,b), W unpriorized (U(-1,1))

    w1 = ((np.random.rand(1000)-0.5)*2)
    w2 = ((np.random.rand(1000)-0.5)*2)
    kappa = np.random.gamma(shape, 1/rate, 1000) 
    # 1a) autocovariance
    ax = axs[0,0]
    ax.hist(kappa + w1**2, 30, density = True,
            label = 'w_1^2 + kappa', color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 1 \nkappa ~Ga(a,b)\n w ~N(-1,1)',
            frameon = False)
    # 1b) cross covariance
    ax = axs[1,0]
    ax.hist(w1*w2, 30, density = True,
            label = 'w_1*w_2', color = 'Blue')
    ## 2
    # RANK 1, kappa ~U(0,1), W ~N(sqrt(a/b),sqrt(a)/b)
    w1 = (np.random.normal(np.sqrt(shape/rate), np.sqrt(shape)/rate, 1000))
    w2 = (np.random.normal(np.sqrt(shape/rate), np.sqrt(shape)/rate, 1000))
    kappa = np.random.rand(1000)
    # 2a) autocovariance
    ax = axs[0,1]
    ax.hist(w1**2+kappa, 30, density = True, label = 'w_1^2 + kappa',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title ='W_rank = 1 \nkappa ~U(0,1)\n w ~N(sqrt(a/b),sqrt(a)/b)',
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
    w1 = np.random.normal(np.sqrt(shape/rate/2), np.sqrt(shape)/rate, 1000)
    w2 = np.random.normal(np.sqrt(shape/rate/2), np.sqrt(shape)/rate, 1000)
    w3 = np.random.normal(np.sqrt(shape/rate/2), np.sqrt(shape)/rate, 1000)
    w4 = np.random.normal(np.sqrt(shape/rate/2), np.sqrt(shape)/rate, 1000)
    # autocovariance
    ax = axs[0,3]
    ax.hist(w1**2+w2**2, 30, density = True,
            label = 'w_11^2 + w_12^2',
        color = 'blue')
    ax.plot(gammax, gammay, label = f'Ga(a,b)', color = 'red', linestyle = 'dashed')
    ax.legend(title = 'W_rank = 2 \nkappa = 0\n w ~N(sqrt(shape/(rate*2)),\n sqrt(shape)/rate))',
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
    # savefig
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