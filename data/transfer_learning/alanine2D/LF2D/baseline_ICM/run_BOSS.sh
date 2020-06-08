#!/bin/bash
#SBATCH --job-name=boss_lf_baseline
#SBATCH --account=project_2000382
#SBATCH --partition=test
#SBATCH --time=00:15:00
#SBATCH --ntasks=1
#SBATCH -o job.out
#SBATCH -e job.err
#####SBATCH --mem-per-cpu=2G

# load environment
module load openbabel/3.0.a1
module load amber/18
unset PYTHONPATH
### execute job (or any script)
export LC_ALL=en_US.utf8
cwd=$(pwd)
cd /projappl/project_2000382/nuutti/BOSSMT
pipenv run ./run_boss.sh $cwd in_2D

