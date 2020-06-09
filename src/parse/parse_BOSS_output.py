import numpy
import json
import os

def parsevalues(line, cast = int, sep = None, idx = 1):
    return [cast(val.strip(sep)) for val in line.split(sep)[idx:]]
def save_to_json(path, filename, expname,json_path = None, json_name = None):
    """
    Parse results ans save dict to json
    path: path to folder where boss.out is
    filename: name of boss output file (boss.out)
    expname: descriptive name of the experiment
    jsonname: name of the json file, defaults to experiment name
    jsonpath: path to folder where json file is to be stored, defaults to path
    """
    res = read_bossout(path, filename, expname)
    if json_name is None:
            json_name = expname
    if json_path is None:
            json_path = path
    with open(os.path.expanduser(f'{json_path}{json_name}.json'),'w') as file:
        print(f'Writing to file: {json_path}{json_name}.json')
        json.dump(res,file)
                       
def read_bossout(path, filename, expname):
    """
    Read boss.out and return results in a dict
    pathname: str, path to folder
    filename: str, name of boss output file (boss.out)
    expname: str, descriptive name of the experiment
    """
    path = os.path.expanduser(path)
    ret = {'name':expname,
            'initpts':None,
          'iterpts':None,
          'num_tasks':1,
           'obs':None,
           'acqtime':None,
           'bestacq':None,
           'gmp': None,
           'gmp_convergence':None,
           'GP_hyperparam':None,
           'itertime':None,
           'totaltime': None
          }
    xy = []
    acqtime = []
    bestacq = []
    gmp = []
    gmp_convergence = []
    gp_hyper = []
    itertime = []
    totaltime = []
    with open(''.join((path,filename)), 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i]
            ret['boss.in'] = lines[20:50]
            if '| Data point added to dataset' in line:
                line = lines[i+1]
                xy.append(parsevalues(line,cast = float,idx = 0))
                
            elif '| Best acquisition' in line:
                line = lines[i+1]
                bestacq.append(parsevalues(line,cast = float,idx = 0))
            
            elif '| Global minimum prediction' in line:
                line = lines[i+1]
                gmp.append(parsevalues(line,cast = float,idx = 0))
            
            elif '| Global minimum convergence' in line:
                line = lines[i+1]
                gmp_convergence.append(parsevalues(line,cast = float,idx = 0))
                
            elif '| GP model hyperparameters' in line:
                line = lines[i+1]
                gp_hyper.append(parsevalues(line,cast = float,idx = 0))
            
            elif 'Iteration time [s]:' in line:
                itertime.append(float(parsevalues(line,cast=str, idx = 3)[0]))
                totaltime.append(parsevalues(line,cast=float, idx = 7)[0])
            
            elif '| Objective function evaluated, time [s]' in line:
                acqtime.append(parsevalues(line,cast=float, idx = 6)[0])
                
            elif 'initpts' in line and ret['initpts'] is None:
                ret['initpts'] = parsevalues(line)
            elif 'iterpts' in line and ret['iterpts'] is None:
                ret['iterpts'] = parsevalues(line)
            elif 'num_tasks' in line:
                ret['num_tasks'] = parsevalues(line)[0]
    
    ret['xy'] = xy
    ret['acqtime'] = acqtime
    ret['bestacq'] = bestacq
    ret['gmp'] = gmp
    ret['gmp_convergence'] = gmp_convergence
    ret['GP_hyperparam'] = gp_hyper
    ret['itertime'] = itertime
    ret['totaltime'] = totaltime

    if len(ret['initpts']) == 1: # add 0 secondary initpts
        ret['initpts'].append(0)
    
    return ret
