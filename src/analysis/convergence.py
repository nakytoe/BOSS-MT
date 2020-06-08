import numpy as np
import json
import yaml
import os
import sys

# use this script to calculate iterations and cpu times to convergence at different levels
"""
---
# yaml input format for calculating convergence for experiments

 - # how long it takes for experiment variables to converge to this value
  true_value: [value]
  tolerance_levels: [list of tolerance levels as absolute differences from true_value]
  variable: string
  begin_row: (int) begin counting from
  select_cols: [list of columns]
  path: str
  experiment_files:
   - 


"""

def calculate_convergence(setup, experiment):
    """
    calculate iterations and cputime to convergence
    """
    experiment['tolerance_levels'] = setup['tolerance_levels']
    experiment['iterations_to_convergence'] = []
    experiment['cputime_to_convergence'] = []
    variable = setup['variable']
    for tolerance_level in experiment['tolerance_levels']:
        values = np.array(experiment[variable])
        # filter rows and columns
        if 'begin_row' in setup:
            values = values[setup['begin_row']:]
        if 'select_cols' in setup:
            values = values[:,setup['select_cols']]
        # calculate difference
        diff = values - np.array(setup['true_value'])
        # calculate iteration of convergence
        i = 0
        for value in diff[::-1]:
            if value > tolerance_level:
                break
            i += 1
        if i == 0:
            iterations_to_convergence = None
            cputime_to_convergence = None
        else:
            iterations_to_convergence = len(values)-i
            cputime_to_convergence = experiment['cputime'][-i]
        experiment['iterations_to_convergence'].append(iterations_to_convergence)
        experiment['cputime_to_convergence'].append(cputime_to_convergence)
        

def load_experiments(setup):
    """
    load experiment data
    """
    path = setup['path']
    experiments = []
    for filename in setup['experiment_files']:
        with open(os.path.expanduser(f'{path}{filename}'), 'r') as f:
            experiment = json.load(f)
            experiments.append(experiment)
    return experiments


def save_results(setup, experiments):
    """
    save results
    """
    path = setup['path']
    for filename, experiment in zip(setup['experiment_files'], experiments):
        with open(os.path.expanduser(f'{path}{filename}'), 'w') as f:
            json.dump(experiment, f)

def main(config):
    for setup in config:

        experiments = load_experiments(setup)

        for experiment in experiments:
            calculate_convergence(setup, experiment)
        save_results(setup, experiments)

if __name__=='__main__':
    args = sys.argv[1:]
    for arg in args:
        with open(arg, 'r') as configfile:
            config = yaml.load(configfile, Loader=yaml.FullLoader)
            main(config)