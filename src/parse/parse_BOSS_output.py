import numpy as np
import json
import os
import sys

def parsevalues(line, typecast = int, sep = None, idx = 1):
    return [typecast(val.strip(sep)) for val in line.split(sep)[idx:]]
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
        ret['boss.in'] = lines[0:100]
        for i in range(len(lines)):
            line = lines[i]
            if '| Data point added to dataset' in line:
                line = lines[i+1]
                xy.append(parsevalues(line,typecast = float,idx = 0))
                
            elif '| Best acquisition' in line:
                line = lines[i+1]
                bestacq.append(parsevalues(line,typecast = float,idx = 0))
            
            elif '| Global minimum prediction' in line:
                line = lines[i+1]
                gmp.append(parsevalues(line,typecast = float,idx = 0))
            
            elif '| Global minimum convergence' in line:
                line = lines[i+1]
                gmp_convergence.append(parsevalues(line,typecast = float,idx = 0))
                
            elif '| GP model hyperparameters' in line:
                line = lines[i+1]
                gp_hyper.append(parsevalues(line,typecast = float,idx = 0))
            
            elif 'Iteration time [s]:' in line:
                itertime.append(float(parsevalues(line,typecast=str, idx = 3)[0]))
                totaltime.append(parsevalues(line,typecast=float, idx = 7)[0])
            
            elif '| Objective function evaluated, time [s]' in line:
                acqtime.append(parsevalues(line,typecast=float, idx = 6)[0])
                
            elif 'initpts' in line and ret['initpts'] is None:
                ret['initpts'] = parsevalues(line)
            elif 'iterpts' in line and ret['iterpts'] is None:
                ret['iterpts'] = parsevalues(line)
            elif 'num_tasks' in line:
                ret['num_tasks'] = parsevalues(line)[0]
            elif 'bounds' in line:
                bounds = parsevalues(' '.join(parsevalues(line, typecast = str,
                                             idx = 1)), typecast = 'str',sep = ';')
                ret['bounds']  =  [parsevalues(bound) for bound in bounds]
            elif 'kernel' in line:
                ret['kernel'] = parsevalues(line, typecast = str, idx = 1)
            elif 'yrange' in line:
                ret['yrange'] = parsevalues(line, typecast = str, idx = 1)
            elif 'thetainit' in line:
                ret['thetainit'] = parsevalues(line, typecast = str, idx = 1)
            elif 'thetapriorparam' in line:
                priorparams = parsevalues(' '.join(parsevalues(line, typecast = str,
                                            idx = 1)), typecast = 'str', sep = ';')
                ret['thetapriorparam'] = [parsevalues(priorparam, typecast = float) for priorparam in priorparams]
    ret['tasks'] = len(np.unique(np.array(xy)[:,-2]))
    if  ret['tasks'] not in [1,2,3]: # old boss
        ret['tasks'] = 1
        ret['dim'] = len(xy[0])-1
    else: # task source included
        ret['dim'] = len(xy[0])-2
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

if __name__=='__main__':
    ### give boss.out and output.json as parameters
    args = sys.argv[1:]
    infile = args[0]
    expname = args[1]
    outfile = args[2].split('.json')[0]
    print("input: ", infile)
    print("output: ", outfile)
    save_to_json('', infile, expname, '', outfile)
