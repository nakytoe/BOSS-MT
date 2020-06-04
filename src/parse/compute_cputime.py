import yaml
import json
import os, sys


"""
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
   -

"""

def compute_cputime(experiment, exptype):
    """
    Function to read parsed boss.out json files, compute single core cpu time 
    approximations to those and save the results in the same file.
    """
    path = os.path.expanduser(str(experiment['path']))
    if exptype == 'single_output':
        for name, single_core_time in zip(experiment['names'], experiment['single_core_time']):
            data = None
            with open(f'{path}{name}.json', 'r') as file:
                data = json.load(file)
                
            if data is not None: # write to file
                N = len(data['acqtime'])
                data['modeltime'] = [itertime-acqtime for itertime, acqtime in zip(data['itertime'], data['acqtime'])]
                data['cputime'] = [sum(data['modeltime'][:i])+(i+1)*single_core_time for i in range(N)]
                with open(f'{path}{name}.json', 'w') as file:
                    json.dump(data, file)
            
    elif exptype == 'transfer_learning':
        name = experiment['namebase']
        for i in range(1,experiment['N_experiments']+1):
            data = None
            with open(f'{path}{name}{i}.json', 'r') as file:
                data = json.load(file)
            if data is not None:
                initpts_cputimes = []
                initpts_list = data['initpts']
                # load cpu times for initpts
                for baseline, initpts in zip(experiment['baselines'], initpts_list):
                    with open(f'{path}{baseline}.json','r') as file:
                        data = json.load(file)
                        if 'cputime' in data:
                            initpts_cputimes.append(data['cputime'][:initpts])
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
                
                with open(f'{path}{name}{i}.json', 'w') as file:
                    json.dump(data, file)
        
        
        
    else:
        raise NotImplementedError(f'unknown experiment type: {exptype} \n compute_cputime not implemented')
        

def main(config):
    types = ['single_output', 'transfer_learning']
    for exptype in types:
        if exptype in config:
            for experiment in config[exptype]:
                compute_cputime(experiment, exptype)
                    


if __name__=='__main__':
    # run with python3 compute_cputime.py config.yaml
    args = sys.argv
    configfile = args[1]
    with open(configfile, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        main(config)