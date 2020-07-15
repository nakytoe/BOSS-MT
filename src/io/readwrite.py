import json
import yaml

def load_json(path, filename):
    """
    load json file
    """
    with open(f'{path}{filename}', 'r') as f:
        data = json.load(f)
        return data
    raise FileNotFoundError(f'{path}{filename} could not be loaded with json.load')

def save_json(data, path, filename):
    """
    save json file
    """
    with open(f'{path}{filename}', 'w') as f:
        json.dump(data, f)

def load_yaml(path, filename):
    """
    load yaml file
    """
    with open(f'{path}{filename}', 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
        
