import numpy as np
import matplotlib.pyplot as plt
import json
import sys

def load_data(filepath):
    with open(filepath,'r') as f:
        data = json.load(f)
    return data

def load_folder(foldername, namebasis, N_exp):
    # load experiment folder
    exp_list = []
    for i in range(1,N_exp+1):
        exp_list.append(load_data(f'{foldername}/{namebasis}_{i}.json'))
    return exp_list

def experiments_mean_sd(experiments, variable, idx, use_abs = False):
    # calculate mean, std and range for a variable
    var = []
    for exp in experiments:
        var.append(np.atleast_2d(np.array(exp[variable]))[:,idx])
    var = np.array(var)
    if use_abs:
        var = np.abs(var)
    m = np.mean(var, axis = 0)
    sd = np.std(var, axis = 0)
    least = np.min(var, axis = 0)
    most = np.max(var, axis = 0)
    return m, sd, least, most

"""
plot results for sobol vs random initialization comparison
this is used to see how much data effects the variability of the results compared to
hyperparameter fitting process
"""

a1a3 = load_folder('processed_data/a1a3', 'exp', 30)
a1a2 = load_folder('processed_data/a1a2', 'exp', 30)

fig, axs = plt.subplots(1,2,
                        figsize = (10,5),
                       sharey = 'all', sharex = 'all')

folders = [a1a2, a1a3]
inittypes = ['identical sobol initialization', 'random (uniform) initialization'] 
for i in range(2):
    # kappa
    ax = axs[i]
    m, sd, least, most = experiments_mean_sd(folders[i],
                            'GP_hyperparam', 2)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    if np.all(least <= m -sd): # when kappa encodes variance
        ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{1+i}) {title}: {inittypes[i]}', loc = 'left')
    ax.set_ylabel('variance')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()

plt.savefig('figures/random_sobol_init_variance_variability.pdf')


"""
Plot results for 1 task heuristics
"""
# load data


a2a1 = load_folder('processed_data/a2a1', 'exp', 30)
a2a2 = load_folder('processed_data/a2a2', 'exp', 30)
a2a3 = load_folder('processed_data/a2a3', 'exp', 30)
a2a4 = load_folder('processed_data/a2a4', 'exp', 30)

fig, axs = plt.subplots(5,3,
                        figsize = (15,15),
                       sharey = 'all', sharex = 'all')

folders = [a1a3, a2a1, a2a2, a2a3, a2a4]

# plot 1st row without kappa and B (baseline)
for ax in axs[0,:2]:
    ax.axis('off')
    
if True:
    i = 0
    ax = axs[i,2]
    m, sd, least, most = experiments_mean_sd(folders[i],
                                'GP_hyperparam', 2,
                                use_abs = True)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{i+1}c) {title}', loc = 'left')
    ax.set_ylabel('variance')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()

# plot rest of the experiments
for i in range(1,5):
    # kappa
    ax = axs[i,0]
    m, sd, least, most = experiments_mean_sd(folders[i],
                            'GP_hyperparam', 3)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    if np.all(least <= m -sd): # when kappa encodes variance
        ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{1+i}a) {title}', loc = 'left')
    ax.set_ylabel('kappa')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()
    
    # W
    ax = axs[i,1]
    m, sd, least, most = experiments_mean_sd(folders[i],
                                'GP_hyperparam', 2,
                                use_abs = True)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{1+i}b) {title}', loc = 'left')
    ax.set_ylabel('|w|')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()
    
    # autocovariance
    ax = axs[i,2]
    m, sd, least, most = experiments_mean_sd(folders[i],
                                'B', 0,
                                use_abs = True)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{1+i}c) {title}', loc = 'left')
    ax.set_ylabel('autocovariance')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()

    plt.savefig('figures/prior_heuristic_results_1_task.pdf')

########
#
### plot  2 task results (autocovariances and cross covariance)
# compare to baselines

a3b1 = load_folder('processed_data/a3b1', 'exp', 30)
a3b2 = load_folder('processed_data/a3b2', 'exp', 30)
a3b3 = load_folder('processed_data/a3b3', 'exp', 30)
a3b4 = load_folder('processed_data/a3b4', 'exp', 30)
a3b5 = load_folder('processed_data/a3b5', 'exp', 30)
a1b2 = load_folder('processed_data/a1b2', 'exp', 30)

fig, axs = plt.subplots(6,3,
                        figsize = (15,18),
                       sharey = 'all', sharex = 'all')

folders = [a1b2, None, a1a3, a3b1, a3b2, a3b3, a3b4, a3b5]

### baselines
for ax, i, enum in zip(axs[0,:], range(3), ['a','b', 'c']):
    if folders[i] is None:
        ax.axis('off')
    else:
        m, sd, least, most = experiments_mean_sd(folders[i],
                                'GP_hyperparam', 2)
        x = np.arange(1, len(m)+1)
        ax.plot(x,m, color = 'black', label = 'mean')
        ax.plot(x,m+sd, color = 'blue',
                linestyle = 'dashed', label = 'sd')
        ax.plot(x,m-sd, color = 'blue', 
                linestyle = 'dashed')
        ax.plot(x,most, color = 'grey',
                linestyle = 'dotted', label = 'range')
        ax.plot(x,least, color = 'grey', linestyle = 'dotted')
        title = folders[i][0]['name'].split('_')[0]
        ax.set_title(f'1{enum}) {title}', loc = 'left')
        ax.set_ylabel('variance')
        ax.set_xlabel('BO iteration')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.legend()

### TL experiments

for i in range(3,8):
    # kappa
    ax = axs[i-2,0]
    m, sd, least, most = experiments_mean_sd(folders[i],
                            'B', 0)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{i-1}a) {title}', loc = 'left')
    ax.set_ylabel('HF autocovariance')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()
    
    # W
    ax = axs[i-2,1]
    m, sd, least, most = experiments_mean_sd(folders[i],
                                'B', 1,
                                use_abs = True)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{i-1}b) {title}', loc = 'left')
    ax.set_ylabel('cross covariance')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()
    
    # b
    ax = axs[i-2,2]
    m, sd, least, most = experiments_mean_sd(folders[i],
                                'B', 3,
                                use_abs = True)
    x = np.arange(1, len(m)+1)
    ax.plot(x,m, color = 'black', label = 'mean')
    ax.plot(x,m+sd, color = 'blue',
            linestyle = 'dashed', label = 'sd')
    ax.plot(x,m-sd, color = 'blue', 
            linestyle = 'dashed')
    ax.plot(x,most, color = 'grey',
            linestyle = 'dotted', label = 'range')
    ax.plot(x,least, color = 'grey', linestyle = 'dotted')
    title = folders[i][0]['name'].split('_')[0]
    ax.set_title(f'{i-1}c) {title}', loc = 'left')
    ax.set_ylabel('LF autocovariance')
    ax.set_xlabel('BO iteration')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.legend()
    
    plt.savefig('figures/prior_heuristic_results_2_task.pdf')