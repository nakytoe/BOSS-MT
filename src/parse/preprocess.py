import yaml
import json
import os, sys
import numpy as np

def get_bestacq(data):
    """
    return point x and output f(x) for lowest observed best acquisition
    """
    return np.array(data['bestacq'])[-1,:]


def y_offset(data):
    """
    Function to offset y values
    """
    y_offset = np.array(data['truemin'])[:,-1]

    for val in data['gmp']:
        val[-2] = (val[-2]-y_offset[0])

    for val in data['bestacq']:
        val[-1] = (val[-1]-y_offset[0])

    for i in range(len(y_offset)):
        for val in data['xy']:
            if i == 0: # primary data 
                val[-1] = (val[-1]-y_offset[i])
            elif len(y_offset) > 0 and val[-2] == i: # there are multiple sources and data is secondary
                val[-1] = (val[-1]-y_offset[i])



def calculate_convergence(data, varname, idx):
    """
    calculates index of variable (from the rear),
    after which the variable is less or equalthan the tolerance
    if the very last value of the variable is larger than tolerance, None is given
    if no value is larger, N is returned

    then, calculates BO iteration and total runtime for convergence at given level 
    """
    # select right column and reverse the order
    values = np.atleast_2d(data[varname])[:,idx][::-1]
    data[f'iterations_to_{varname}_convergence'] = [] # BO iterations
    data[f'totaltime_to_{varname}_convergence'] = [] # total runtime
    data[f'observations_to_{varname}_convergence'] = [] # total number of observations, including initpts
    
    for tolerance in data['tolerance_levels']:
        i = 0
        for value in values:
            if value > tolerance:
                break
            i += 1
        if i == 0:
            iterations_to_convergence = None
            totaltime_to_convergence = None
            observations_to_convergence = None
        else:
            iterations_to_convergence = len(values)-i
            totaltime_to_convergence = data['totaltime'][-i]
            observations_to_convergence = len(data['xy'])-i
        data[f'iterations_to_{varname}_convergence'].append(iterations_to_convergence)
        data[f'totaltime_to_{varname}_convergence'].append(totaltime_to_convergence)
        data[f'observations_to_{varname}_convergence'].append(observations_to_convergence)

def calculate_B(data):
    dim = data['dim']
    if dim == len(data['xy'][0])-1:
        data['B'] = None
    else:
        data['B'] = []
        tasks = data['tasks']
        for row in data['GP_hyperparam']:
            W = np.array(row[dim:-tasks]).reshape((-1,tasks))
            Kappa = np.diag(row[-tasks:])
            B = W.dot(W.T) + Kappa
            data['B'].append([b for b in B.flatten()])

def add_inittimes(data, initial_data_cost):
    """
    Add computational cost from initialization data
    """
    accounted_initpts = 0
    for cost, initpts in zip(initial_data_cost, data['initpts']):
        if cost is None: # if initialization has been through active acquisition
            pass
        else: # if initialization data has been taken from a baseline
            begin = accounted_initpts
            if accounted_initpts != 0:
                begin -= 1
            end = begin + initpts
            for i in range(begin, end):
                data['totaltime'][i] += cost[i-begin]
            for i in range(end, len(data['totaltime'])):
                data['totaltime'][i] += cost[initpts-1]
            
        accounted_initpts += initpts


def preprocess(data, tolerance_levels = [0], initial_data_cost = None):
    """
    optionally add time taken for initialization data (acquisition time)
    calculate model time
    center and rescale output so that best acq of baseline is 0
    calculate convergence 
    """

    data['modeltime'] = [itertime-acqtime for itertime, acqtime in zip(data['itertime'], data['acqtime'])]

    # add possible exra cost for initialization data
    if initial_data_cost is not None:
        add_inittimes(data, initial_data_cost)

    
    
    ### offset y
    y_offset(data)

    ### gmp convergence
    data['tolerance_levels'] = tolerance_levels
    calculate_convergence(data, varname = 'gmp', idx = -2)

    # calculate B
    calculate_B(data)
    
    return data
   
