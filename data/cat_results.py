import numpy as np
import random
import sys

def clean_hyperparameters(data, xdim):
    """
    clean hyperparameters from data, just to be sure
    """
    for i in range(len(data)):
        data[i] = ' '.join(data[i].split()[:xdim+1])
    return data

def load_from(filepath):
    """
    Read observations from boss.rst
    """
    ret = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        results = False
        for line in lines:
            if results:
                ret.append(line)
            elif 'RESULTS:' in line:
                results = True
            else:
                pass
    return ret

def add_task_index(data, xdim, idx):
    """
    Add task index to observations
    """
    for i in range(len(data)):
        line = data[i]
        values = line.split()
        values.insert(xdim, f'{idx}')
        values.append('\n')
        line = ' '.join(values)
        data[i] = line
    return data

def append_to_input(filepath, data):
    """
    Save rst data to boss.in
    """
    # open file in append mode
    with open(filepath, 'a+') as f:
        # seek beginning
        f.seek(0) 
        # read contents
        lines = f.readlines()
        # assume that input file does not have RESULTS line
        has_results = False
        for line in lines:
            # check if RESULTS line in input
            if 'RESULTS:' in line:
                has_results = True
                break
        if not has_results:
            # add RESULTS: before observations
            f.write('RESULTS:\n')
        # write observations to boss.in
        f.writelines(data)

def select_points(data, N, select_by):
    """
    select N vetors from data
    """
    if select_by == 'inorder':
        return data[:N]
    elif select_by == 'random':
        return random.sample(data, k = N)

        
def modify_initpts(filepath, N0, N1):

    """
    modify number of initpts
    """
    lines = None
    with open(filepath, 'r') as f:
        lines = f.readlines()
    with open(filepath, 'w') as f:
        for line in lines:
            if 'initpts' in line:
                line = f'{line.split()[0]} {int(N0)} {int(N1)}\n'
            f.write(line)

def main(inputfile, xdim,
        primary = None, secondary = None,
        N_primary = 0, N_secondary = 0,
        select_by = 'random'):
    """
    Read observations from primary and secondary task
    and append to input file to be used as initialization data.

    primary: primary task boss.out
    secondary: secondary task boss.out
    inputfile: input file to be added initialization data to
    xdim: search space dimensions
    N_primary: number of primary observations to be used
    N_secondary: number of secondary observations to be used
    select_by: strategy to select secondary observations by
                - random: select N points by random
                - inorder: select N points inorder from the beginning
    """
    # modify initpts keyword
    modify_initpts(inputfile, N_primary, N_secondary)

    filepaths = [primary, secondary]
    N_pts = [N_primary, N_secondary]
    for i in range(2):
        # read observations
        filepath = filepaths[i]
        N = N_pts[i]
        if filepath is not None:
            # read data
            data = load_from(filepath)
            print('loaded data:')
            print(data)
            # clean hyperparameters
            data = clean_hyperparameters(data, xdim)
            # select observations
            data = select_points(data, N, select_by)
            # add source
            data = add_task_index(data, xdim, i)
            # write to input
            append_to_input(inputfile, data)



if __name__=='__main__':
    args = sys.argv[1:]
    for arg in args:
        if arg == 'none':
            arg = None
    inputfile = args[0]
    xdim = int(args[1])
    primary = args[2]
    secondary = args[3]
    N_primary = int(args[4])
    N_secondary = int(args[5])
    select_by = args[6]

    main(inputfile, xdim,
        primary, secondary,
        N_primary, N_secondary,
        select_by)