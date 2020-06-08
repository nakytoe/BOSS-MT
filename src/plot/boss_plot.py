import matplotlib.pyplot as plt
import json
import yaml
import numpy as np
import os, sys
import string

# here make general function for plotting variables from boss experiment
BASELINE_COLOR = '#ff0000' # RED
BASELINE_LINESTYLE = 'dashed'
BASELINE_MARKER = 's'

ARRAY_COLOR = '#0000ff'
ARRAY_LINESTYLE = 'solid'
ARRAY_COLORMAP = plt.cm.Blues
ARRAY_MARKER = 'o'

UNIQUE_COLOR = '#0f000f'
UNIQUE_LINESTYLE = 'dashdot'
UNIQUE_MARKER = 'x'

"""
---
# yaml plot input format
figures:
 - 
  path: path where plot is saved
  filename: name of the figure file
  subplots: # plot all plots in 
   - 
    # load data
    path: path to parsed output files
    baseline: none or filename
    array_experiments: none or
      namebase: str
      N_experiments:
      use_colormap: True or False
    unique_experiments: none or
     - filename
     xkey: key of x variable in data
     ykey: key of y variable in data
     xunit: unit of x variable to be plotted
     yunit: unit of y variable to be plotted
     # add more variables
     title: none or subplot title
     legend: True or False
     labelrule: none or 'secondary initpts' or 'name' or invent more
"""

def load_json(path, filename):
    """
    load json file
    """
    filepath = os.path.expanduser(f'{path}{filename}.json')
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data
    print(f'file {path}{filename}.json not found')
    raise FileNotFoundError

def make_label(experiment, labelrule):
    """
    create label for legend
    """
    name = experiment['name']
    if labelrule == 'secondary initpts':
        if len(experiment['initpts']) > 1:
            secondary_initpts = experiment['initpts'][1]
            experiment['label'] = f'{secondary_initpts}'
        else:
            experiment['label'] = f'0 ({name})'
    if labelrule == 'name':
        experiment['label'] = experiment['name']

def add_plot_attributes(experiment, color, linestyle, marker):
    """
    add information required for plotting
    """
    experiment['color'] = color
    experiment['linestyle'] = linestyle
    experiment['marker'] = marker

def plot_preprocessing(subplot):
    """
    return list of experiments with plotting attributes added
    """
    path = subplot['path']
    experiments = []
    # plot an experiment
    if 'array_experiments' in subplot and subplot['array_experiments'] is not None:
        array_experiments = subplot['array_experiments']
        N_experiments = array_experiments['N_experiments']
        for i in range(1, N_experiments+1):
            namebase = array_experiments['namebase']
            experiment = load_json(path, f'{namebase}{i}')
            if array_experiments['use_colormap']:
                initpts = experiment['initpts']
                color = ARRAY_COLORMAP(i/N_experiments)
            else:
                color = ARRAY_COLOR
            add_plot_attributes(experiment, color, ARRAY_LINESTYLE, ARRAY_MARKER)
            experiments.append(experiment)
    # plot a unique experimennt
    if 'baseline' in subplot and subplot['baseline'] is not None:
        baseline_file = subplot['baseline']
        baseline = load_json(path, baseline_file)
        add_plot_attributes(baseline, BASELINE_COLOR, BASELINE_LINESTYLE, BASELINE_MARKER)
        experiments.append(baseline)

    if 'unique_experiments' in subplot and subplot['unique_experiments'] is not None:
        for unique_name in subplot['unique_experiments']:
            unique = load_json(path, unique_name)
            add_plot_attributes(unique, UNIQUE_COLOR, UNIQUE_LINESTYLE, UNIQUE_MARKER)
            experiments.append(unique)
    # add labels
    for experiment in experiments:
        if 'legend' in subplot and 'labelrule' in subplot:
            make_label(experiment, subplot['labelrule'])
        else: experiment['label'] = None

    return experiments


def make_subplot(subplot, ax):
    experiments = plot_preprocessing(subplot)
    N_experiments = len(experiments)
    make_subplots = range(N_experiments)
    if 'make_subplots' in subplot: # user can define explicitely which subplots to show
        make_subplots = subplot['make_subplots']
    # plot baseline

    plottype = 'timeseries'
    if 'plottype' in subplot:
        plottype = subplot['plottype']

    for i in make_subplots:
        experiment = experiments[i]
        # assign variable y
        ykey = subplot['ykey'] # y name
        if 'ycol' in subplot:
            ycol = subplot['ycol'] # y column
            y = np.array(experiment[ykey])[:,ycol]
        else:
            y = np.array(experiment)[ykey]
        if 'ybegin' in subplot:
            ybegin = subplot['ybegin']
            y = y[ybegin:]
        if 'yend' in subplot:
            yend = subplot['yend']
            y = y[:yend]
        ## rescale y if needed
        if 'rescale_y' in subplot:
            y = y*subplot['rescale_y']
        N_y = len(y)
        # assign variable x
        if 'xkey' in subplot:
            xkey = subplot['xkey']
            xcol = subplot['xcol']
            x = experiment[xkey]
            if 'xbegin' in subplot:
                xbegin = subplot['xbegin']
                x = x[xbegin:]
            if 'xend' in subplot:
                xend = subplot['xend']
                x = x[:xend]
            x = np.atleast_2d(x).reshape((len(x), -1))[-N_y:,xcol]
        else:
            x = np.arange(N_y)+1
        
        # setup
        color = experiment['color']
        marker = experiment['marker']
        linestyle = experiment['linestyle']
        label = experiment['label']
        
        # make plot according to selected plot type
        if plottype == 'timeseries':
            ax.plot(x,y, color = color,
            linestyle = linestyle, 
            marker = marker, 
            label = label
            )
        elif plottype == 'scatter':
            ax.scatter(x, y, color = color,
            marker = marker, label = label
            )

    if 'xunit' in subplot:
        ax.set_xlabel(subplot['xunit'])
    
    if 'yunit' in subplot:
        ax.set_ylabel(subplot['yunit'])

    if 'legend' in subplot and subplot['legend']:
        location = None
        if 'legend_location' in subplot:
            location = subplot['legend_location']
        legend_title = None
        if 'legend_title' in subplot:
            legend_title = subplot['legend_title']
        ax.legend(title = legend_title,loc = location)

    
    xmin = None
    xmax = None
    if 'xmin' in subplot:
        xmin =  subplot['xmin']
    if 'xmax' in subplot:
        xmax = subplot['xmax']
    ax.set_xlim(xmin, xmax)
    ymin = None
    ymax = None
    if 'ymin' in subplot:
        ymin =  subplot['ymin']
    if 'ymax' in subplot:
        ymax = subplot['ymax']
    ax.set_ylim(ymin, ymax)

    if 'remove_top_right_spines' in subplot and subplot['remove_top_right_spines']:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    
    

def calculate_plotgrid(figure):
    """
    calculate how large plot grid is required
    return a tuple
    """
    N_subplots = len(figure['subplots'])
    nrow = int(np.sqrt(N_subplots)) # round down 
    ncol = int(np.ceil(N_subplots / nrow))
    return nrow, ncol



def main(config):
    """
    go through list of figures in config and plot them
    """
    for figure in config['figures']: # make figure
        rows, cols = calculate_plotgrid(figure)
        fig, axs = plt.subplots(rows, cols, figsize = (cols*5, rows*5))
        N_subplots = len(figure['subplots'])
        # add subplots
        for subplot, ax, i in zip(figure['subplots'], np.array(axs).flatten()[:N_subplots],range(N_subplots)):
            title = ''
            if 'enumerate_subplots' in figure and figure['enumerate_subplots']:
                title = f'{title}{string.ascii_lowercase[i]})'
            if 'title' in subplot:
                titletext = subplot['title']
                title = f'{title} {titletext}'
            make_subplot(subplot, ax)
            ax.set_title(title, loc = 'left')
        if N_subplots != rows*cols:
            for ax in np.array(axs).flatten()[(N_subplots-rows*cols):]:
                ax.axis('off')
        # save figure
        path = figure['path']
        name = figure['filename']
        filename = os.path.expanduser(f'{path}{name}.pdf')
        plt.savefig(filename)


if __name__=='__main__':
    # run by giving names of yaml config files
    configfilenames = sys.argv[1:]
    for configfilename in configfilenames:
        with open(configfilename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            main(config)
