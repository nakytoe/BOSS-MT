import yaml
import json
import os, sys

def rescale_and_center(data, keyword, rescale_by, truemin, idx):
    """
    Function to rescale and center values
    """
    for val in data[keyword]:
        val[idx] = (val[idx]-truemin)*rescale_by

def preprocess(experiment, exptype):
    """
    Function to read parsed boss.out json files and:
    compute single core cpu time,
    center and rescale output so that best acq of baseline is 0

    finally save the results in the same file.
    
    ---
    # yaml format for cpu time computing

    single_output: # baselines and single experiments
     -
      path: # path to json files
      names: str list # path to experiment names
      single_core_times: float list # approximation acquisition time on single core

    transfer_learning:
     -
      path:
      baselines:
       - name of baseline 1
       - 
      N_experiments:
      namebase:
      single_core_time:
    """
    path = os.path.expanduser(str(experiment['path']))
    if exptype == 'single_output':
        for name, single_core_time, rescale_by, get_truemin_from in zip(experiment['names'],
         experiment['single_core_time'], experiment['rescale_by'], experiment['get_truemin_from']):
            data = None
            with open(f'{path}{name}.json', 'r') as f:
                data = json.load(f)
                
            if data is not None: # write to file
                ### compute cpu time
                N = len(data['acqtime'])
                data['modeltime'] = [itertime-acqtime for itertime, acqtime in zip(data['itertime'], data['acqtime'])]
                data['cputime'] = [sum(data['modeltime'][:i])+(i+1)*single_core_time for i in range(N)]
                
                ### rescale and center
                if get_truemin_from == 'self' or get_truemin_from is None:
                    truemin = data['bestacq'][-1][-1]
                    data['baseline_best_acquisition'] = truemin
                else:
                    with open(f'{path}{get_truemin_from}.json', 'r') as f:
                        truemindata = json.load(f)
                    truemin = truemindata['baseline_best_acquisition']
                
                # bestacq
                rescale_and_center(data, 'bestacq', rescale_by, truemin, -1)
                # gmp mean
                rescale_and_center(data, 'gmp', rescale_by, truemin, -2)
                # gmp variance
                rescale_and_center(data, 'gmp', rescale_by**2, 0, -1)
                # observations y
                rescale_and_center(data, 'xy', rescale_by, truemin, -1)

                with open(f'{path}{name}.json', 'w') as f:
                    print(f'Writing to file: {path}{name}.json')
                    json.dump(data, f)
            
    elif exptype == 'transfer_learning':
        name = experiment['namebase']
        for i in range(1,experiment['N_experiments']+1):
            data = None
            with open(f'{path}{name}{i}.json', 'r') as f:
                data = json.load(f)
            if data is not None:
                initpts_cputimes = []
                initpts_list = data['initpts']
                # load cpu times for initpts
                for baseline, initpts in zip(experiment['baselines'], initpts_list):
                    with open(f'{path}{baseline}.json','r') as f:
                        baseline_data = json.load(f)
                        if 'cputime' in baseline_data:
                            initpts_cputimes.append(baseline_data['cputime'][:initpts])
                        else:
                            raise ValueError(f'cputime not computed for baseline: {path}{baseline}')

                for j in range(len(initpts_cputimes[1])): # add cumulative cpu time to initpts
                    initpts_cputimes[1][j] += initpts_cputimes[0][-1]
                
                data['cputime'] = []
                for cputimes in initpts_cputimes:
                    for cputime in cputimes:
                        data['cputime'].append(cputime)
                init_cputime_sum = data['cputime'][-1]
                # Compute cpu times for experiments           
                single_core_time = experiment['single_core_time']
                N = len(data['acqtime'])
                data['modeltime'] = [itertime-acqtime for itertime, acqtime in zip(data['itertime'][-N:], data['acqtime'])]
                for j in range(N):
                    data['cputime'].append(sum(data['modeltime'][:j])+(j+1)*single_core_time + init_cputime_sum)
                


                ### rescale and center for primary baseline
                rescale_by = experiment['rescale_by']
                baseline = experiment['baselines'][0]
                with open(f'{path}{baseline}.json','r') as f:
                    baseline_data = json.load(f)
                    
                    truemin = baseline_data['baseline_best_acquisition']

                    # bestacq
                    rescale_and_center(data, 'bestacq', rescale_by, truemin, -1)
                    # gmp mean
                    rescale_and_center(data, 'gmp', rescale_by, truemin, -2)
                    # gmp variance
                    rescale_and_center(data, 'gmp', rescale_by**2, 0, -1)
                    # observations y
                    rescale_and_center(data, 'xy', rescale_by, truemin, -1)

                with open(f'{path}{name}{i}.json', 'w') as f:
                    print(f'Writing to file: {path}{name}{i}.json')
                    json.dump(data, f)
        
        
        
    else:
        raise NotImplementedError(f'unknown experiment type: {exptype} \n compute_cputime not implemented')
        

def main(config):
    types = ['single_output', 'transfer_learning']
    for exptype in types:
        if exptype in config:
            for experiment in config[exptype]:
                preprocess(experiment, exptype)
                    


if __name__=='__main__':
    # run with python3 compute_cputime.py config.yaml
    args = sys.argv
    configfile = args[1]
    with open(configfile, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        main(config)