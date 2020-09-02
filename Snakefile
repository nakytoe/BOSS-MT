
import numpy as np
import src.io.readwrite as rw
import src.parse.parse_BOSS_output as parse
import src.parse.preprocess as preprocess
import src.analyse.sumstat as sumstat
import src.plot.plot_convergence as plot_convergence

import os

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
                # read truemin values from baselines
                for baseline_folder in experiments[folder]:
                    baseline_file = PARSED_DICT[baseline_folder][0]
                    data = rw.load_json(f'processed_data/{baseline_folder}/',f'{baseline_file}.json')
                    truemin.append(data['truemin'][0])
                # save truemin values to experiments
                for filename in PARSED_DICT[folder]:
                    data = rw.load_json(f'processed_data/{folder}/',f'{filename}.json')
                    data['truemin'] = truemin
                    data = preprocess.preprocess(data, tolerances)
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
        'figures/scatter_trellis_alanine2D.pdf',
        'figures/scatter_trellis_alanine4D.pdf'
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
            # plot scatter trellis
            sumstat.plot_y_scatter_trellis(explist, f'figures/scatter_trellis_{saveto}.pdf')


rule prior_hypothesis:
    """
    visualize prior hypothesis
    independent from experiment data
    """
    output:
        "figures/prior_hypothesis_1_task_shape_2_amplitude_10.pdf",
        "figures/prior_hypothesis_2_task_shape_2_amplitude_10.pdf",
        "figures/prior_hypothesis_sumstat_amplitude.pdf"
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
        "figures/prior_heuristic_results_1_task.pdf",
        "figures/prior_heuristic_results_2_task.pdf",
        "figures/random_sobol_init_variance_variability.pdf",
        "figures/prior_selection_convergence_1_task.pdf",
        "figures/prior_selection_convergence_2_task.pdf",
        "figures/prior_selection_convergence_random_sobol.pdf"
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
                plot_convergence.plot_convergence_iter_time_distraction(folders, f'figures/{figurename}.pdf')


