import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import scipy.stats as ss
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline



def loewner(A, B):
    """
    Return true, if A>=B
    where >= is loewner order (matrix comparison) 
    if A>=B, A spans over B
    used to detect poor fits of coregionalization
    if [coregionalization matrix] > [measured covariance]is broken, 
    covariance matrix is overestimated / fitted poorly
    """
    ret_list = []
    for b in B:
        D = (A-b).reshape((2,2))
        det = np.linalg.det(D)
        ret = 1
        if det < 0 or D[0,0] < 0:
            ret = 0
        ret_list.append(ret)
    return ret_list
        

def plot_TL_convergence(filename, experiment_folders, baseline_folders):
    """
    Plot for list of TL experiments:
    convergence speed to 0.1 kcal/mol in
    - BO iterations and CPU time
    - mean of both (statistical expected value)
    - linear trend
    """
    cputime_max = 0
    N = len(experiment_folders)
    fig, axs = plt.subplots(2,N,
                    figsize = (5*N,10),
                    sharey = 'row')
    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    LARGE_SIZE = 25

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=LARGE_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize

    for i in range(N):
        experiment = experiment_folders[i].copy()
        baseline = baseline_folders[i].copy()

        explist = baseline
        for exp in experiment:
            explist.append(exp)


        convergence_iterations = []
        convergence_times = []

        for exp in explist:
            if len(exp['initpts'])>1:
                secondary_initpts = int(exp['initpts'][1])
            else:
                secondary_initpts = 0
            # convergence by iteration
            convergence_iter = exp['iterations_to_gmp_convergence'][5]
            convergence_iterations.append([secondary_initpts,convergence_iter])
            # convergence by cpu time
            convergence_time = exp['totaltime_to_gmp_convergence'][5]
            convergence_times.append([secondary_initpts, convergence_time])
            
           

        # plot
        convergence_iterations = np.array(convergence_iterations, dtype = float)
        axs[0, i].scatter(convergence_iterations[:,0],
                          convergence_iterations[:,1],
                    color = 'blue', alpha = 0.5, marker = 'x',
                         label = 'observation')

        # linear fit
        raw_rows = convergence_iterations
        clean_rows = raw_rows[np.logical_not(np.logical_or(np.isnan(raw_rows[:,0]),
                                                           np.isnan(raw_rows[:,1]))),:]
        x_train = clean_rows[:,0].reshape(-1,1)
        y_train = clean_rows[:,1].reshape(-1,1)
        reg = LinearRegression().fit(x_train, y_train)
        x = np.unique(convergence_iterations[:,0]).reshape(-1,1)
        y = reg.predict(x)
        axs[0, i].plot(x,y, color = 'red', label = 'trend', linewidth = 3)
        # plot means
        mean_labelled = False
        for initpts in np.unique(x_train):
            mean = np.mean(y_train[x_train == initpts])
            if mean_labelled:
                axs[0,i].scatter([initpts], [mean], color = 'red', marker = 's')
            else:
                axs[0,i].scatter([initpts], [mean],
                                 color = 'red', marker = 's',
                                label = 'mean')
                mean_labelled = True
        axs[0,i].legend()

        ###
        convergence_times = np.array(convergence_times, dtype = float)
        axs[1, i].scatter(convergence_times[:,0],
                          convergence_times[:,1],
                    color = 'blue', alpha = 0.5, marker = 'x',
                         label = 'observation')
        ### linear fit
        raw_rows = convergence_times
        clean_rows = raw_rows[np.logical_not(np.logical_or(np.isnan(raw_rows[:,0]),
                                                           np.isnan(raw_rows[:,1]))),:]
        clean_rows = clean_rows.reshape(-1,2)
        #outliers = clean_rows[clean_rows[:,1] > cputime_max,:]
        # outlier if more than 2 stds off the mean
        outlier_idx = []
        for row in clean_rows:
            initpts = row[0]
            val = row[1]
            obs = clean_rows[clean_rows[:,0] == initpts,:]
            #obs = obs[obs != row]
            m = np.mean(obs)
            sd = np.std(obs)
            if (val - m) / sd > 2.5: # z-score - assuming normal
                # distribution only 0.5% of data should be at least this far
                outlier_idx.append(True)
            else:
                outlier_idx.append(False)
        outliers = clean_rows[outlier_idx, :]
        #clean_rows = clean_rows[clean_rows[:,1] <= cputime_max, :]
        clean_rows = clean_rows[np.logical_not(outlier_idx),:]
        if max(clean_rows[:,1]) > cputime_max:
            cputime_max = max(clean_rows[:,1])
        x_train = clean_rows[:,0].reshape(-1,1)
        y_train = clean_rows[:,1].reshape(-1,1)

        degree=1
        polyreg=make_pipeline(PolynomialFeatures(degree),LinearRegression())
        polyreg.fit(x_train,y_train)

        x = np.unique(convergence_iterations[:,0]).reshape(-1,1)
        axs[0,i].set_xticks(x[::2])
        y = polyreg.predict(x)
        axs[1, i].plot(x,y, color = 'red', label = 'trend', linewidth = 3)
        axs[1,i].set_xticks(x[::2])
        outlier_labelled = False
        for outlier in outliers:
            if outlier_labelled:
                axs[1,i].scatter([outlier[0]],[cputime_max*1.1],
                             marker = 6, color = 'black')
            else:
                axs[1,i].scatter([outlier[0]],[cputime_max*1.1],
                             marker = 6, color = 'black',
                            label = 'outlier')
                outlier_labelled = True
            axs[1,i].annotate('{:.0f}'.format(outlier[1]), 
                              [outlier[0],cputime_max*1.1], rotation = 270)
        mean_labelled = False
        for initpts in np.unique(x_train):
            mean = np.mean(y_train[x_train == initpts])
            if mean_labelled:
                axs[1,i].scatter([initpts], [mean], color = 'red', marker = 's')
            else:
                axs[1,i].scatter([initpts], [mean],
                                 color = 'red', marker = 's',
                                label = 'mean')
                mean_labelled = True
        axs[1,i].legend()

        expname = experiment_folders[i][0]['name'].split('_')[0]
        title = f'{i+1}a) {expname}'
        axs[0,i].set_title(title, loc = 'left')
        title = f'{i+1}b) {expname}'
        axs[1,i].set_title(title, loc = 'left')



    axs[0,0].set_ylabel('BO iterations to GMP convergence')
    axs[1,0].set_ylabel('CPU time to GMP convergence')

    axs[1,0].set_ylim(-0.05*cputime_max,1.4*cputime_max)

    for ax in axs[1,:]:
        ax.set_xlabel('secondary initpts')

    for ax in axs.flatten():
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params('x',labelrotation = 40)
        ax.tick_params(axis = 'both',
              width = 3, length = 4)

    plt.savefig(filename)
    
    