
import numpy as np
import src.io.readwrite as rw
import src.parse.parse_BOSS_output as parse
import src.parse.preprocess as preprocess
import src.analyse.sumstat as sumstat

import os

# define all inputs and outputs

# RAW boss.out
RAW_wildcard = glob_wildcards('data/experiments/{raw_name}/boss.out')
RAW_NAME = RAW_wildcard.raw_name



## RULES
rule all:
    input:
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME),
        'results/tables/sobol_sumstat.tex'
        
# UNPREPROCESSED boss.out
        # detect folders
if True:
    if True:
        PARSED_wildcard = glob_wildcards('processed_data/{exp_folder}/{exp_file}.json')
        PARSED_FOLDERS = np.unique(list(PARSED_wildcard.exp_folder))
        print(PARSED_FOLDERS)
        # detect files inside folders
        PARSED_FILELISTS = [] # list of lists of files inside each folder
        for folder in PARSED_FOLDERS:
            searchstring = ''.join([f'processed_data/{folder}/','{exp_file}.json'])
            parsed_filelist = glob_wildcards(searchstring).exp_file
            PARSED_FILELISTS.append(parsed_filelist)

        PARSED_DICT = {}
        for folder, filelist in zip(PARSED_FOLDERS, PARSED_FILELISTS):
            PARSED_DICT[folder] = filelist

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
            print(folder)
            bestacqs = []
            get_truemin_from = baselines[folder]
            for filename in PARSED_DICT[get_truemin_from]: # load all baseline experiments
                print(filename)
                data = rw.load_json(f'processed_data/{folder}/',f'{filename}.json')
                bestacq = preprocess.get_bestacq(data)
                bestacqs.append(bestacq)
            # select lowest observed value
            bestacqs = np.array(bestacqs)
            truemin = [list(bestacqs[np.argmin(bestacqs[:,-1]),:])]
            # save truemin ad y_offset and offset all y values accordingly
            for filename in PARSED_DICT[folder]: # load all baseline experiments
                data = rw.load_json(f'processed_data/{folder}/',f'{filename}.json')
                data['truemin'] = truemin
                data = preprocess.preprocess(data, tolerances)
                rw.save_json(data, f'processed_data/{folder}/',f'{filename}.json')
                    
        # other experiments
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
    input:
        'src/config/analysis/sumstat.yaml',
        expand('processed_data/{raw_name}.json',
                raw_name = RAW_NAME)
    output:
        'results/tables/sobol_sumstat.tex'
    run:
        config = rw.load_yaml('src/config/analysis/', 'sumstat.yaml')
        sobol_folders = []
        for foldername in config['sobol']:
            sobol_folder = []
            for filename in PARSED_DICT[foldername]:
                data = rw.load_json(f'processed_data/{foldername}/',f'{filename}.json')
                sobol_folder.append(data)
            sobol_folders.append(sobol_folder)
        table, colnames, rownames = sumstat.summarize_folders_fx(sobol_folders)
        rw.write_table_tex(table, output[0], colnames, rownames)