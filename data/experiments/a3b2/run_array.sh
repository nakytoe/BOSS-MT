#!/bin/bash
### run an array job of experiments

#BATCH --job-name=a3b2
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
# add primary and secondary data to input file
inputfile='exp_'${SLURM_ARRAY_TASK_ID}'/in_2D'
xdim=2
primary='../a1b2_baseline_random_init/exp_'${SLURM_ARRAY_TASK_ID}'/boss.rst'
secondary='../../LF2D/a1a3_baseline_random_init/exp_'${SLURM_ARRAY_TASK_ID}'/boss.rst'
N0=2
N1=30
selectby='random'
python3 ~/cat_results.py $inputfile $xdim $primary $secondary $N0 $N1 $selectby 

cd exp_${SLURM_ARRAY_TASK_ID}
./run_BOSS.sh
cd ..

