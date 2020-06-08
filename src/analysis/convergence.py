import numpy
import json
import yaml
import os
import sys

# use this script to calculate iterations and cpu times to convergence at different levels
"""
---
# yaml input format for calculating convergence for experiments
final_value:
 - # how long it takes for experiment variables to converge to this value
  true_value: [value]
  tolerance_levels: [list of tolerance levels as absolute differences from true_value]
  variable: string
  variable_begin: (int) begin counting from
  variable_cols: [list of columns]

"""


if __name__=='__main__':
    args = sys.argv[1:]
    for arg in args:
        with open(arg, 'r') as configfile:
            config = yaml.load(configfile)