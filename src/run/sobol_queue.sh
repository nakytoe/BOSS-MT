#!/bin/bash
cwd=$pwd
cd ~/BOSS-MT/src
python3 parse/parse_files.py config/parse_sobol_queue.yaml
python3 parse/preprocess.py config/preprocess_sobol_queue.yaml
cd $cwd  
