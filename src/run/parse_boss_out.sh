#!/bin/bash

### This is a script for parsing out boss.out files from experiments
### the files are determined by config/parse_boss_out.yaml
### the outputs are stored in processed_data/ as json files

python3 ~/BOSS-MT/src/parse/parse_files.py ~/BOSS-MT/src/config/parse_boss_out.yaml
