import json
import yaml
import sys
import os

### functions for parsing out experiment information in a table




def save_csv():
    pass
def save_tex():
    pass


def main(config):
    """
    read selected attributes from data and tabularise them.
    save result in selected format.
    """

if __name__=='__main__':
    args = sys.argv[1:] # read configuration file full paths
    for configfilepath in args: # loop through
        with open(os.path.expanduser(configfilepath), 'r') as configfile: # read configuration file
            config = yaml.load(configfile, Loader=yaml.FullLoader) # load tabularise configuration
            main(config)


