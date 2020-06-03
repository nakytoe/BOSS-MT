import yaml
import sys
from parse_BOSS_output import save_to_json


"""
---
# yaml format

unique:
 - experiment:
  path: (str)
  json_path: (srt) or none
  files:
   - (str)
  names:
   - (str)
  
array:
 - experiment:
  path: (str)
  N_experiments: (int)
  namebase: (str)
  json_path: (str) or none

"""

def parse_to_json(config):
    # single experiments, like baselines
    if 'unique' in config:
        for experiment in config['unique']:
            path = experiment['path']
            json_path = experiment['json_path']
            for file, name in zip(experiment['files'], experiment['names']):
                save_to_json(path, file, name, json_path = json_path, json_name = None)
    if 'array' in config:
        for experiment in config['array']:
            path = experiment['path']
            N = experiment['N_experiments']
            filebase = experiment['filebase']
            namebase = experiment['namebase']
            json_path = experiment['json_path']
            for i in range(1, N+1):
                save_to_json(path,f'{filebase}{i}/boss.out', f'{namebase}{i}',
                             json_path = json_path, json_name = None)     

if __name__=='__main__':
    args = sys.argv
    with open(args[1],'r') as file:
        config = yaml.load(file)
        parse_to_json(config)