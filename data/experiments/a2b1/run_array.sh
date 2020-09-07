#!/bin/bash
### run an array job of experiments

#BATCH --job-name=a2b1
#SBATCH --account=project_2000382
#SBATCH --array=1-30
#SBATCH --partition=small
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH -o job/job%A_%a.out
#SBATCH -e job/job%A_%a.err
#####SBATCH --mem-per-cpu=2G

# copy template 
scp -r template exp_${SLURM_ARRAY_TASK_ID}
cd exp_${SLURM_ARRAY_TASK_ID}
./run_BOSS.sh
cd ..

