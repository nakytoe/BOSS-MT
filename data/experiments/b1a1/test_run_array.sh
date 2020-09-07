#!/bin/bash
### run an array job of experiments

#BATCH --job-name=b1a1
#SBATCH --account=project_2000382
#SBATCH --array=1
#SBATCH --partition=test
#SBATCH --time=00:15:00
#SBATCH --ntasks=1
#SBATCH -o job/job%A_%a.out
#SBATCH -e job/job%A_%a.err
#####SBATCH --mem-per-cpu=2G

scp -r template exp_${SLURM_ARRAY_TASK_ID}

cd exp_${SLURM_ARRAY_TASK_ID}
./run_BOSS.sh
cd ..
