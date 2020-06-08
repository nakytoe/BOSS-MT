#!/bin/bash

### This is a script for parsing out boss.out files from experiments
### the files are determined by config/parse_boss_out.yaml
### the outputs are stored in processed_data/ as json files

### preprocessing step 1: parse data from boss.out
python3 ~/BOSS-MT/src/parse/parse_files.py ~/BOSS-MT/src/config/parse_boss_out.yaml
### preprocessing step 2: compute model and cpu times
python3 ~/BOSS-MT/src/parse/compute_cputime.py ~/BOSS-MT/src/config/compute_cputime.yaml    
### calculate iterations of convergence
###python3 ~/BOSS-MT/src/analysis/convergence.py ~/BOSS-MT/src/config/calculate_convergence.yaml
