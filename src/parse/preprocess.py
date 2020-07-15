import yaml
import json
import os, sys

def get_bestacq(data):
    """
    return point x and output f(x) for lowest observed best acquisition
    """
    return data['bestacq'][-1,:]

def offset(data, keyword, truemin, idx):
    """
    Function to offset values
    """
    for val in data[keyword]:
        val[idx] = (val[idx]-truemin)

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
            if value > tolerance_level:
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
        data[f'iterations_to_{varname}_convergence'].append(totaltime_to_convergence)
        data[f'observations_to_{varname}_convergence'].append(observations_to_convergence)

def preprocess(data, truemin = 0, tolerance_levels = [0]):
    """
    calculate model time
    center and rescale output so that best acq of baseline is 0
    calculate convergence 
    """
    N = len(data['acqtime'])
    data['modeltime'] = [itertime-acqtime for itertime, acqtime in zip(data['itertime'], data['acqtime'])]
    
    ### offset
    for keyword, idx in zip(['bestacq', 'gmp', 'xy'], [-1,-2,-1])
        offset(data, keyword, truemin idx)

    ### gmp convergence
    data['tolerance_levels'] = tolerance_levels
    calculate_convergence(data, varname = 'gmp', idx = -2)
    
    return data
   
