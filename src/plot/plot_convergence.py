import numpy as np
import matplotlib.pyplot as plt 

def plot_convergence_iter_time_distraction(folders, filename):
    """
    Given list of experiment data, plot
    convergence against bo iteration, 1 core cpu time and distraction rate
    
    distraction rate is the proportion of experiments that do not reach given 
    convergence level
    """
    N = len(folders)
    fig, axs = plt.subplots(N, 3, figsize = (15,3*N),
                           sharey = 'all', sharex = 'col',
                           constrained_layout = True)
    SMALL_SIZE = 15
    MEDIUM_SIZE = 20
    LARGE_SIZE = 30

    for i in range(N):
        
        ### BO iteration
        ax = axs[i,0]
        folder = folders[i]
        tolerances = []
        times = []
        tolerances_lists = []
        times_lists = []
        for exp in folder:
            tolerances_list = []
            times_list = []
            for tolerance, totaltime in zip(exp['tolerance_levels'], exp['iterations_to_gmp_convergence']):
                tolerances.append(tolerance)
                times.append(totaltime)
                tolerances_list.append(tolerance)
                times_list.append(totaltime)
            tolerances_lists.append(tolerances_list)
            times_lists.append(times_list)
        title = folder[0]['name'].split('_')[0]
        ax.set_title(f'{i+1}a) {title}', loc = 'left', fontsize = LARGE_SIZE)
        ax.scatter(times, tolerances, marker = 'x',
                   color = 'blue', alpha = 0.5,
                    label = 'observation')

        times_lists = np.array(times_lists, dtype = float)
        times_mean = np.nanmean(times_lists, axis = 0)

        tolerances_lists = np.array(tolerances_lists, dtype = float)
        tolerances_mean = np.nanmean(tolerances_lists, axis = 0)
        ax.plot(times_mean, tolerances_mean, color = 'red',
             marker = 's', label = 'mean')

        ax.set_xlabel('BO iteration', fontsize = MEDIUM_SIZE)
        ax.set_ylabel('GMP conv. (kcal/mol)', fontsize = SMALL_SIZE)
        ax.set_yscale('log')
        ax.legend(fontsize = SMALL_SIZE)
        ### cpu time
        ax = axs[i,1]
        folder = folders[i]
        tolerances = []
        times = []
        tolerances_lists = []
        times_lists = []
        for exp in folder:
            tolerances_list = []
            times_list = []
            for tolerance, totaltime in zip(exp['tolerance_levels'], exp['totaltime_to_gmp_convergence']):
                tolerances.append(tolerance)
                times.append(totaltime)
                tolerances_list.append(tolerance)
                times_list.append(totaltime)
            tolerances_lists.append(tolerances_list)
            times_lists.append(times_list)
        title = folder[0]['name'].split('_')[0]
        ax.set_title(f'{i+1}b) {title}', loc = 'left', fontsize = LARGE_SIZE)
        ax.scatter(times, tolerances, marker = 'x',
                   color = 'blue', alpha = 0.5,
                    label = 'observation')

        times_lists = np.array(times_lists, dtype = float)
        times_mean = np.nanmean(times_lists, axis = 0)

        tolerances_lists = np.array(tolerances_lists, dtype = float)
        tolerances_mean = np.nanmean(tolerances_lists, axis = 0)
        ax.plot(times_mean, tolerances_mean, 'r', marker = 's', label = 'mean')
        ax.set_xlabel('CPU time (s)', fontsize = MEDIUM_SIZE)
        ax.set_ylabel('GMP conv. (kcal/mol)', fontsize = SMALL_SIZE)
        ax.set_yscale('log')
        ax.legend(fontsize = SMALL_SIZE)

        ### Distraction rate
        # proportion of experiments that do not converge to a given tolerance level
        ax = axs[i,2]
        folder = folders[i]
        tolerances = []
        times = []
        tolerances_lists = []
        times_lists = []
        for exp in folder:
            tolerances_list = []
            times_list = []
            for tolerance, totaltime in zip(exp['tolerance_levels'], exp['totaltime_to_gmp_convergence']):
                tolerances.append(tolerance)
                times.append(totaltime)
                tolerances_list.append(tolerance)
                times_list.append(totaltime)
            tolerances_lists.append(tolerances_list)
            times_lists.append(times_list)
        title = folder[0]['name'].split('_')[0]
        ax.set_title(f'{i+1}c) {title}', loc = 'left', fontsize = LARGE_SIZE)

        times_lists = np.array(times_lists, dtype = float)
        distraction_rate = np.count_nonzero(np.isnan(times_lists), axis = 0)/len(times_lists)

        tolerances_lists = np.array(tolerances_lists, dtype = float)
        tolerances_mean = np.nanmean(tolerances_lists, axis = 0)
        ax.barh(tolerances_mean, distraction_rate,
                height = tolerances_mean*0.5, align='center',
               color = 'grey')
        ax.set_xlabel('distraction rate', fontsize = MEDIUM_SIZE)
        ax.set_ylabel('GMP conv. (kcal/mol)', fontsize = SMALL_SIZE)
        ax.set_yscale('log')
        

    for ax in axs.flatten():
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis = 'both',
              width = 3, length = 4, labelsize = SMALL_SIZE)
        ax.set_ylim(0.0005, 10)


    axs[0,2].set_xlim(0,1)

    plt.savefig(filename)