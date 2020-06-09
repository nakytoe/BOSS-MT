#!/bin/bash

cwd=$HERE
cd ~/BOSS-MT/src

python3 plot/boss_plot.py config/plot_bestacq_by_BO_iteration.yaml
python3 plot/boss_plot.py config/plot_gmp_by_BO_iteration.yaml
python3 plot/boss_plot.py config/plot_gmp_variance_by_BO_iteration.yaml
python3 plot/boss_plot.py config/plot_last_gmp_x.yaml
python3 plot/boss_plot.py config/plot_convergence.yaml

cd $cwd
