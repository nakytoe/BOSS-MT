import json
import yaml
import sys
import os
import pandas as pd
### functions for parsing out experiment information in a table

"""
---
# tabularise yaml format
tables:
 - 
  table_header: str
  table_subeaders: str
  path_to_data: str
  experiments:
    single: none or
     - str (name)
    array: none or
     - 
      namebase:
      N_experiments:
  columns: none or # if none, list of experiments (above) will be used
   - srt
  rows: none or
   - str # see columns

  save_to_path: str
  table_filename: str

"""



def save_csv():
    pass
def save_tex():
    pass
def save_pd_json():
    pass

def load_data(path, filename):
    experiments = []
    with open(os.path.expanduser(f'{path}{filename}'), 'r') as f:
        experiment = json.load(f)
        experiments.append(experiment)
    return experiments

def tabularise(table):
    """
    read selected attributes from data to pd dataframe.
    save result in selected format.
    """
    path_to_data = os.path.expanduser(table['path_to_data'])
    df_list = [] # list of data frames
    keys = []
    if 'single' in table['experiments']:
        for filename in table['experiments']['single']:
            with open(f'{path_to_data}{filename}.json', 'r') as f: 
                new_df = pd.read_json(f)
                df_list.append(new_df)
                keys.append(new_df['name'])
    data = pd.concat(df_list, keys)
    

if __name__=='__main__':
    args = sys.argv[1:] # read configuration file full paths
    for configfilepath in args: # loop through
        with open(os.path.expanduser(configfilepath), 'r') as configfile: # read configuration file
            config = yaml.load(configfile, Loader=yaml.FullLoader) # load tabularise configuration
            for table in config['tables']:
                tabularise(table)


