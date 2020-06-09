#!/bin/bash

### This is a script for parsing out boss.out files from experiments
### the files are determined by config/parse_boss_out.yaml
### the outputs are stored in processed_data/ as json files

cdw=$HERE

cd ~/BOSS-MT/src

### preprocessing step 1: parse data from boss.out
python3 parse/parse_files.py config/parse_boss_out.yaml
### preprocessing step 2: compute model and cpu times
python3 parse/compute_cputime.py config/compute_cputime.yaml    
### calculate iterations of convergence
python3 analysis/convergence.py config/calculate_convergence.yaml
