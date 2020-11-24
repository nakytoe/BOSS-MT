import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import kruskal
from scipy.stats import chi2
import sys

np.random.seed(328)

# command line call parameters
args = sys.argv[1:]

loss_table_path = args[0]
loss_plot_path = args[1]
indicator_loss_plot_path = args[2]
loss_boolean_conversion_plot_path = args[3]
confusion_matrix_path = args[4]

loss_table = pd.read_csv(loss_table_path)

# for the plots
SMALL_SIZE = 15
MEDIUM_SIZE = 20
LARGE_SIZE = 25

### MEAN LOSS FUNCTION MINIMUM

fig, ax = plt.subplots(1,figsize = (10,10))
positions = []
res = pd.DataFrame(columns = ['initpts','min_loss','expname'])
for expname in np.unique(loss_table['experiment']):
    exp = loss_table
    exp = exp[exp['experiment'] == expname]
    min_loss = min(exp['mean_loss'])
    loss = exp[exp['mean_loss'] == min_loss]['mean_loss']
    initpts = exp[exp['mean_loss'] == min_loss]['secondary_initpts']
    indicator_loss = exp[exp['mean_loss'] == min_loss]['indicator_loss']
    res = pd.concat([res,pd.DataFrame(data = {'initpts':[initpts.iloc[0]],
                                       'min_loss':[loss.iloc[0]],
                                       'expname':[expname],
                                        'indicator_loss':indicator_loss.iloc[0]})])
    
select_color = lambda x: 'black' if x else 'red'
select_marker = lambda x: 's' if x else 'x'
for indicator in [True, False]:
    legendtext = 'faster than baseline'
    if not indicator:
        legendtext = f'not {legendtext}'
    res[res['indicator_loss'] == indicator].plot(kind = 'scatter',
         x = 'initpts', 
         y = 'min_loss', 
         ax = ax, s = 50,
         color = select_color(indicator),
         marker = select_marker(indicator),
        label = legendtext)
legend = ax.legend(title = 'indicator loss function', fontsize = MEDIUM_SIZE)
plt.setp(legend.get_title(),fontsize=LARGE_SIZE)
# add text labels
prev = None
xadd = 0
yadd = 0
direction = 1
for _,row in res.sort_values(by = ['min_loss', 'initpts'], ascending = False).iterrows():
    # if there is overlap, move up
    
    if prev is not None:
        xdiff = (prev['min_loss']-row['min_loss'])
        ydiff = (prev['initpts']-row['initpts'])
        if np.abs(xdiff) < 0.05 and np.abs(ydiff) < 20:
            xadd += 5*direction
            yadd -= 0.02
            yadd *= direction
            direction*=-1
        else:
            xadd = 0
            yadd = 0
    ax.plot([row['initpts'],row['initpts']+xadd],
            [row['min_loss'],row['min_loss']+yadd],
           color = select_color(row['indicator_loss']))
    
    ax.annotate(' ' + row['expname'],
                xy = [row['initpts']+xadd,row['min_loss']+yadd],
               fontsize = MEDIUM_SIZE, rotation = 0, va = 'center_baseline',
               color = select_color(row['indicator_loss']))
    prev = row

ax.set_ylim(ymin = 0)
ax.set_xlim(xmin = 0)
ax.set_xlabel('secondary initpts', fontsize = LARGE_SIZE)
ax.set_ylabel('loss function minimum', fontsize = LARGE_SIZE)
ax.tick_params(axis = 'both', labelsize = MEDIUM_SIZE)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.savefig(loss_plot_path)

#### INDICATOR LOSS FUNCTION

SMALL_SIZE = 15
MEDIUM_SIZE = 20
LARGE_SIZE = 25
fig, ax = plt.subplots(1,figsize = (10,10))
idx = 0
expnames = np.sort(np.unique(loss_table['experiment']))
labelled = False
for expname in expnames:
    exp = loss_table[loss_table['experiment'] == expname]
    loss = exp['indicator_loss']
    faster = exp[loss == 1]['secondary_initpts']
    slower = exp[loss == 0]['secondary_initpts']
    f_height = np.full(len(faster), idx)
    s_height = np.full(len(slower), idx)
    if labelled:
        ax.scatter(faster, f_height, color = 'black', marker = 's')
        ax.scatter(slower, s_height, color = 'red', marker = 'x')
    else:
        ax.scatter(faster, f_height, color = 'black', marker = 's',
                   label = 'faster than baseline')
        ax.scatter(slower, s_height, color = 'red', marker = 'x',
                   label = 'not faster than baseline')
        labelled = True
    idx += 1
ax.tick_params(axis = 'both', labelsize = MEDIUM_SIZE)
ax.set_yticks(np.arange(idx))
ax.set_yticklabels(expnames)
ax.set_ylabel('experiment', fontsize = LARGE_SIZE)
ax.set_xlabel('secondary initpts', fontsize = LARGE_SIZE)
#ax.set_title('indicator loss function', fontsize = LARGE_SIZE)
legend = ax.legend(title = 'indicator loss function',
          fontsize = MEDIUM_SIZE)
plt.setp(legend.get_title(),fontsize=LARGE_SIZE)

plt.savefig(indicator_loss_plot_path)

### LOSS FUNCTION BOOLEAN CONVERSION

SMALL_SIZE = 15
MEDIUM_SIZE = 20
LARGE_SIZE = 25
fig, ax = plt.subplots(1,figsize = (10,10))
idx = 0
expnames = np.sort(np.unique(loss_table['experiment']))
is_faster = lambda x: True if x < 1 else False
loss_table['loss_boolean_conversion'] = loss_table['mean_loss'].apply(is_faster) 
labelled = False
for expname in expnames:
    exp = loss_table[loss_table['experiment'] == expname]
    loss = exp['loss_boolean_conversion']
    faster = exp[loss == 1]['secondary_initpts']
    slower = exp[loss == 0]['secondary_initpts']
    f_height = np.full(len(faster), idx)
    s_height = np.full(len(slower), idx)
    if labelled:
        ax.scatter(faster, f_height, color = 'black', marker = 's')
        ax.scatter(slower, s_height, color = 'red', marker = 'x')
    else:
        ax.scatter(faster, f_height, color = 'black', marker = 's',
                   label = 'faster than baseline')
        ax.scatter(slower, s_height, color = 'red', marker = 'x',
                   label = 'not faster than baseline')
        labelled = True
    idx += 1
ax.tick_params(axis = 'both', labelsize = MEDIUM_SIZE)
ax.set_yticks(np.arange(idx))
ax.set_yticklabels(expnames)
ax.set_ylabel('experiment', fontsize = LARGE_SIZE)
ax.set_xlabel('secondary initpts', fontsize = LARGE_SIZE)
#ax.set_title('indicator loss function', fontsize = LARGE_SIZE)
legend = ax.legend(title = 'loss function\nboolean conversion',
          fontsize = MEDIUM_SIZE)
plt.setp(legend.get_title(),fontsize=LARGE_SIZE)

plt.savefig(loss_boolean_conversion_plot_path)

### CONFUSION MATRIX

# to see which method is more conservative

# calculate confusion matrix
# diagonal: count how many true values
# cross diagonal: count how many are true, but are not true in the alternative

def textabline(row):
    line = ' & '.join(row)
    line = f'{line} \\\\ \n'
    return line
def write_table_tex(table, filepath, colnames = None, rownames = None):
    lines = []
    with open(filepath, 'w') as f:
        if rownames is not None:
            lines.append(textabline(rownames))
        if colnames is None:
            for row in table:
                row = ['{:.3f}'.format(val) for val in row]
                lines.append(textabline(row))
        else:
            for row, colname in zip(table, colnames):
                row = ['{:.3f}'.format(val) for val in row]
                row.insert(0, colname)
                lines.append(textabline(row))
        f.writelines(lines)

def confusion_matrix(data):
    ret = np.array([[0,0],[0,0]])
    # set diagonal values
    for i in [0,1]:
        ret[i,i] = np.count_nonzero(data[data.columns[i]])
    
    ret[0,1] = np.count_nonzero(np.logical_and(data[data.columns[0]],
                                np.logical_not(data[data.columns[1]])))
    ret[1,0] = np.count_nonzero(np.logical_and(data[data.columns[1]],
                                np.logical_not(data[data.columns[0]])))


    return ret, data.columns[:2]

cm, variables = confusion_matrix(loss_table[['loss_boolean_conversion','indicator_loss']])
write_table_tex(cm, confusion_matrix_path, colnames = variables, rownames = variables)

## ANOVA for detecting if there are differnces in 2D methods

# first combine all loss functions to see if there are differences
# stack all experiments with same initialization strategy in same order

def query_by_strategy(df, strategy_list):
    ret = df.query('experiment in @strategy_list')
    return ret['mean_loss'].values

def nonparametric_ANOVA(data, column_names, alpha = 0.05):
    """
    Recursively perform nonparametric ANOVA
    first, with kruskal wallis to see if there are differences
    then, if there are pairwise differences, with wilcoxon find which is faster
    """
    namestring = ', '.join(column_names)
    print(f'Performing nonparametric ANOVA')
    print(f'Kruskal-Wallis({namestring})')
    print('H0: there is no statistical difference between the columns')

    to_be_tested = []
    for name in column_names:
        to_be_tested.append(data[name])
    ksw_res = kruskal(*to_be_tested)
    print(f'Result: {ksw_res}')
    # test statistical significance
    g = len(column_names)
    deg_free = g-1
    critical_value = chi2.ppf(ksw_res.pvalue, deg_free)
    print(f'Critical value: {critical_value}')
    ksw_rejected = ksw_res.statistic > critical_value
    if ksw_rejected:
        print('-- H0 REJECTED: there is statistically significant difference between the columns')
    else:
        print('-- H0 ACCEPTED: there is no statistically significant difference between the columns')

    ret = pd.DataFrame({'strategy':column_names,'faster_count':0})
    faster = None
    if g >= 3:
        # recursively iterate through all combinations
        for name in column_names:
            res = nonparametric_ANOVA(data, column_names[column_names != name])
            ret = pd.concat([ret,res])
    elif g == 2 and ksw_rejected: # pairwise comparison
        print('-- Performing pairwise comparison with Wilcoxon signed rank test')
        print(f'   H0: {column_names[0]} is faster than {column_names[1]}')
        wx_res = wilcoxon(data[column_names[0]], data[column_names[1]],
                 alternative = 'greater')
        print(f'   Result: {wx_res}')
        if wx_res.pvalue > alpha:
            faster = column_names[0]
            print(f'   -- H0 ACCEPTED: {column_names[0]} is faster than {column_names[1]}')
        else:
            faster = column_names[1]
            print(f'   -- H0 REJECTED: {column_names[1]} is faster than {column_names[0]}')
    else:
        # individual comparison of the pairs
        pass
    if faster is not None:
        N = len(ret)
        ret = pd.concat([ret, pd.DataFrame({'strategy':faster, 'faster_count':1}, index = [N])])
    return ret

### 2D

initstrategies = pd.DataFrame()

initstrategies['random'] = query_by_strategy(loss_table,["a3b9", "a3c7", "a3c8"])
initstrategies['sobol'] = query_by_strategy(loss_table,["a3b8", "a3c5", "a3c6"])
initstrategies['BO_inorder'] = query_by_strategy(loss_table,["a3b7", "a3c3", "a3c4"])
initstrategies['BO_random'] = query_by_strategy(loss_table,["a3b6", "a3c1", "a3c2"])

fast_count = nonparametric_ANOVA(initstrategies, initstrategies.columns)

for strategy in fast_count['strategy'].unique():
    count = sum(fast_count[fast_count['strategy'] == strategy]['faster_count'])
    print(f'{strategy} {count}')

### 4D

initstrategies = pd.DataFrame()
initstrategies['BO_inorder'] = query_by_strategy(loss_table,["b3b1", "b3c1", "b3c2"])
initstrategies['BO_random'] = query_by_strategy(loss_table,["b3b2", "b3c3", "b3c4"])
fast_count = nonparametric_ANOVA(initstrategies, initstrategies.columns)
for strategy in fast_count['strategy'].unique():
    count = sum(fast_count[fast_count['strategy'] == strategy]['faster_count'])
    print(f'{strategy} {count}')