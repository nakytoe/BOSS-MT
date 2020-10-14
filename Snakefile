
import numpy as np
import pandas as pd
import src.io.readwrite as rw
import src.parse.parse_BOSS_output as parse
import src.parse.preprocess as preprocess
import src.analyse.sumstat as sumstat
import src.plot.plot_convergence as plot_convergence
import src.plot.plot_TL_results as plot_TL_results
import os
import matplotlib.pyplot as plt


# define all inputs and outputs

# RAW boss.out
RAW_wildcard = glob_wildcards('data/experiments/{raw_name}/boss.out')
RAW_NAME = RAW_wildcard.raw_name
PARSED_DICT = {}
for rawname in RAW_NAME:
    exp_folder = rawname.split('/')[0]
    exp = rawname.split('/')[1]
    if exp_folder not in PARSED_DICT:
        PARSED_DICT[exp_folder] = [exp]
    else:
        PARSED_DICT[exp_folder].append(exp)
## RULES
rule all:
    input:
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME),
        'results/tables/sobol_sumstat.tex'
        
# UNPREPROCESSED boss.out
        # detect folders


# parse data from boss.out
rule parse_and_preprocess:
    input:
        'src/config/parse_and_preprocess/preprocess.yaml',
        expand('data/experiments/{raw_name}/boss.out',
                raw_name = RAW_NAME)
        
    output:
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME)
    run:
        # parse
        for infile, rawname, outfile in zip(input[1:], RAW_NAME, output):
            outfile = f'{outfile}'
            name = '_'.join(rawname.split('/exp_'))
            parse.parse(infile, name, outfile)

        
        # preprocess
        config = rw.load_yaml('src/config/parse_and_preprocess/','preprocess.yaml')
        tolerances = config['tolerances']
        # baselines
        baselines = config['baselines']
        for folder in list(baselines.keys()): # loop through baselines
            bestacqs = []
            get_truemin_from = baselines[folder]
            truemin_precalculated = None
            for filename in PARSED_DICT[get_truemin_from]: # load all baseline experiments
                data = rw.load_json(f'processed_data/{get_truemin_from}/',f'{filename}.json')
                bestacq = preprocess.get_bestacq(data)
                bestacqs.append(bestacq)
                if 'truemin' in data: # if truemin has been calculated, use it
                    print(data['truemin'])
                    truemin_precalculated = data['truemin']
                    break
            # select lowest observed value
            if truemin_precalculated is None:
                bestacqs = np.array(bestacqs)
                truemin = [list(bestacqs[np.argmin(bestacqs[:,-1]),:])]
            else:
                truemin = truemin_precalculated
            # save truemin ad y_offset and offset all y values accordingly
            for filename in PARSED_DICT[folder]: # load all baseline experiments
                data = rw.load_json(f'processed_data/{folder}/',f'{filename}.json')
                data['truemin'] = truemin
                data = preprocess.preprocess(data, tolerances)
                rw.save_json(data, f'processed_data/{folder}/',f'{filename}.json')
                    
        # other experiments
        if 'experiments' in config:
            experiments = config['experiments']
            for folder in list(experiments.keys()):
                truemin = []
                # number of experiments
                N_exp = len(PARSED_DICT[folder])
                baseline_plustimes = [] # table of additional times per source
                # read truemin values from baselines
                for i in range(len(experiments[folder])):
                    baseline_plustime = []
                    baseline_folder = experiments[folder][i][0]
                    initstrategy = experiments[folder][i][1]
                    baseline_file = PARSED_DICT[baseline_folder][0]
                    data = rw.load_json(f'processed_data/{baseline_folder}/',f'{baseline_file}.json')
                    truemin.append(data['truemin'][0])
                    # for approximating computational cost for initialization data
                    if initstrategy == 'self': # total time is true computational cost
                        baseline_plustime = None
                    elif initstrategy == 'random': # there is no heavy process for selecting secondary data, only the cost of acquisitions
                        for baseline_file in PARSED_DICT[baseline_folder]:
                            data = rw.load_json(f'processed_data/{baseline_folder}/',f'{baseline_file}.json')
                            plustime = data['acqtime'].copy()
                            for i in range(len(data['acqtime'])):
                                plustime[i] += sum(np.array(data['acqtime'])[:i]) # cumulative cost
                            baseline_plustime.append(plustime)
                    elif initstrategy == 'inorder': # in addition to acquisition cost, there is cost of BO of the initalization data
                        for baseline_file in PARSED_DICT[baseline_folder]:
                            data = rw.load_json(f'processed_data/{baseline_folder}/',f'{baseline_file}.json')
                            baseline_plustime.append(data['totaltime'].copy())
                    else:
                        raise ValueError("unknown initstrategy")
                    baseline_plustimes.append(baseline_plustime)
                # save truemin values to experiments

                for i in range(len(PARSED_DICT[folder])):
                    initial_data_cost = []
                    for baseline_plustime in baseline_plustimes:
                        if baseline_plustime is None:
                            initial_data_cost.append(None)
                        else:
                            N_baselines = len(baseline_plustime)
                            initial_data_cost.append(baseline_plustime[(i % N_baselines)])
                    filename = PARSED_DICT[folder][i]
                    data = rw.load_json(f'processed_data/{folder}/',f'{filename}.json')
                    data['truemin'] = truemin
                    data = preprocess.preprocess(data, tolerances, initial_data_cost)
                    rw.save_json(data, f'processed_data/{folder}/',f'{filename}.json')
            
rule sumstat:
    # calculate summary statistics for the experiments
    input:
        'src/config/analysis/sumstat.yaml',
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME)
    output:
        'results/tables/sobol_sumstat.tex',
        'results/tables/covariance_alanine2D.tex',
        'results/tables/covariance_alanine4D.tex',
        'results/figures/scatter_trellis_alanine2D.pdf',
        'results/figures/scatter_trellis_alanine4D.pdf',
        'results/figures/mean_acquisition_times.pdf',
        'results/tables/acquisition_time_ratios.tex',
        'results/figures/TL_initialization_strategies.pdf',
        'results/figures/baseline_convergence_alanine2D.pdf',
        'results/tables/baseline_convergence_alanine2D.tex',
        'results/figures/baseline_convergence_alanine4D.pdf',
        'results/tables/baseline_convergence_alanine4D.tex'
    run:
        config = rw.load_yaml('src/config/analysis/', 'sumstat.yaml')
        # calculate summary statistics for sobol experiments
        sobol_folders = []
        for foldername in config['sobol']:
            sobol_folder = []
            for filename in PARSED_DICT[foldername]:
                data = rw.load_json(f'processed_data/{foldername}/',f'{filename}.json')
                sobol_folder.append(data)
            sobol_folders.append(sobol_folder)
        table, colnames, rownames = sumstat.summarize_folders_fx(sobol_folders)
        rw.write_table_tex(table, output[0], colnames, rownames)
        # calculate true covariances and correlation from sobol experiments
        for expnamelist in config['covariance']:
            explist = []
            names = []
            saveto = expnamelist[0]
            # load data
            for expname in expnamelist[1]:
                for filename in PARSED_DICT[expname]:
                    data = rw.load_json(f'processed_data/{expname}/',f'{filename}.json')
                    explist.append(data)
                    names.append(data['name'])
            print(names)
            # covariance
            covariance_matrix = sumstat.calculate_covariance(explist)
            rw.write_table_tex(covariance_matrix, f'results/tables/covariance_{saveto}.tex', colnames = names, rownames = names)
            # Pearson's correlation coefficient
            corr_matrix = sumstat.calculate_correlation(explist)
            rw.write_table_tex(corr_matrix, f'results/tables/correlation_{saveto}.tex', colnames = names, rownames = names)
            # plot scatter trellis, to verify that pearsons is a valid measure of correlation
            sumstat.plot_y_scatter_trellis(explist, f'results/figures/scatter_trellis_{saveto}.pdf')
        
        # plot mean acquisition times
        folders = []
        for expname in config['timings']:
            filename = PARSED_DICT[expname][0]
            data = rw.load_json(f'processed_data/{expname}/',f'{filename}.json')
            folders.append([data])
        timing_ratios = sumstat.timings_plot_table('results/figures/mean_acquisition_times.pdf', folders)
        # make table of acquisition time ratios
        with open('results/tables/acquisition_time_ratios.tex', 'w') as f:
            f.writelines(timing_ratios)

        # compare TL sampling strategies
        folders = []
        for expname in config['sampling_strategies']:
            #filename = PARSED_DICT[expname][0]
            data = rw.load_json(f'processed_data/{expname}/',f'exp_1.json')
            folders.append([data])
        sumstat.plot_TL_initialization_strategies('results/figures/TL_initialization_strategies.pdf', folders)
        
        # plot baseline convergence speeds & do statistical testing of the distributions
        for namebase in config['baseline_convergence_speed'].keys():
            folders = []
            for expname in config['baseline_convergence_speed'][namebase]:
                folder = []
                for filename in PARSED_DICT[expname]:
                    data = rw.load_json(f'processed_data/{expname}/',f'{filename}.json')
                    folder.append(data)
                folders.append(folder)
            sumstat.baseline_convergence_speed(f'results/figures/{namebase}.pdf',
                            f'results/tables/{namebase}.tex', folders)

rule prior_hypothesis:
    """
    visualize prior hypothesis
    independent from experiment data
    """
    output:
        "results/figures/prior_hypothesis_1_task_shape_2_amplitude_10.pdf",
        "results/figures/prior_hypothesis_2_task_shape_2_amplitude_10.pdf",
        "results/figures/prior_hypothesis_sumstat_amplitude.pdf"
    shell:
        "python3 src/plot/plot_w_kappa_prior_hypothesis.py 2 10 {output}"
    
rule prior_selection_results:
    """
    Plot results for testing prior hypothesis
    """
    input:
        'src/config/plot/prior_selection_convergence.yaml',
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME)
    output:
        "results/figures/prior_heuristic_results_1_task.pdf",
        "results/figures/prior_heuristic_results_2_task.pdf",
        "results/figures/random_sobol_init_variance_variability.pdf",
        "results/figures/prior_selection_convergence_1_task.pdf",
        "results/figures/prior_selection_convergence_2_task.pdf",
        "results/figures/prior_selection_convergence_random_sobol.pdf"
    run:
        # hyperparam distributions
        # the following line will cause a warning. Apparently launching another python script 
        # that makes graphs is hazardous. However, it still works so I let it be.
        os.system("python3 src/plot/plot_hyperparam_prior_results.py")
        # convergence
        config = rw.load_yaml('src/config/plot/','prior_selection_convergence.yaml')
        if 'figures' in config:
            for figurename in config['figures'].keys():
                folders = []
                for foldername in config['figures'][figurename]:
                    folder = []
                    for filename in PARSED_DICT[foldername]:
                        data = rw.load_json(f'processed_data/{foldername}/',f'{filename}.json')
                        folder.append(data)
                    folders.append(folder)
                plot_convergence.plot_convergence_iter_time_distraction(folders, f'results/figures/{figurename}.pdf')

rule plot_tl_results:
    """
    plot results for tl experiments
    - convergence speed to 0.1 kcal/mol
    """
    input:
        'src/config/plot/plot_TL_results.yaml',
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME)
    output:
        'results/figures/convergence_alanine2D_TL_BO_random_init.pdf',
        'results/figures/convergence_alanine2D_TL_BO_inorder_init.pdf',
        'results/figures/convergence_alanine2D_TL_sobol_init.pdf',
        'results/figures/convergence_alanine2D_TL_random_init.pdf',
        'results/figures/convergence_alanine4D_TL_BO_inorder_init.pdf',
        'results/figures/convergence_alanine4D_TL_BO_random_init.pdf',
        'processed_data/loss_table.csv',
        'results/tables/loss_table.tex'
    run:
        # load plot configuration
        def load_experiments(exp_name):
            folder = []
            for filename in PARSED_DICT[exp_name]:
                data = rw.load_json(f'processed_data/{exp_name}/',f'{filename}.json')
                folder.append(data)
            return folder
        config = rw.load_yaml('src/config/plot/','plot_TL_results.yaml') 
        print(config)
        tot_loss_table = None
        for plotname in config['plotnames'].keys():
            print(plotname)
            # load experiments
            experiments = [load_experiments(exp_name) for exp_name in config['plotnames'][plotname]['experiments']]
            # load baselines
            baselines = [load_experiments(exp_name) for exp_name in config['plotnames'][plotname]['baselines']]
            # plot convergence
            loss_table = plot_TL_results.plot_TL_convergence(f'results/figures/convergence_{plotname}.pdf', experiments, baselines)
            if tot_loss_table is None:
                tot_loss_table = loss_table
            else:
                tot_loss_table = pd.concat([tot_loss_table, loss_table])
        # save loss function to csv
        tot_loss_table.to_csv('processed_data/loss_table.csv')
        rw.write_table_tex(loss_table.values[:,1:],'results/tables/loss_table.tex',
            colnames = loss_table.columns.values[1:].astype(str),
            rownames = loss_table.values[:,0].astype(str))
        
rule evaluate_loss:
    """
    Plot and compare loss functions
    """
    input:
        'processed_data/loss_table.csv',
        'src/plot/plot_loss_functions.py'
    output:
        'results/figures/loss_minimas.pdf',
        'results/figures/indicator_loss.pdf',
        'results/figures/loss_boolean_conversion.pdf',
        'results/tables/boolean_indicator_loss_confusion.txt',
        'results/evaluate_loss.txt'
    run:
        outfiles = ' '.join(output)
        os.system('touch results/evaluate_loss.txt')
        os.system(f'python3 src/plot/plot_loss_functions.py {input[0]} {outfiles} >> results/evaluate_loss.txt')