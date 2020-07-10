#!/bin/bash
### run an array job of experiments

#BATCH --job-name=boss
#SBATCH --account=project_2000382
#SBATCH --array=1-16
#SBATCH --partition=small
#SBATCH --time=64:00:00
#SBATCH --ntasks=20
#SBATCH -o job/job%A_%a.out
#SBATCH -e job/job%A_%a.err
#####SBATCH --mem-per-cpu=2G
scp -r exp_template exp_${SLURM_ARRAY_TASK_ID}
cd exp_${SLURM_ARRAY_TASK_ID}

if [ ${SLURM_ARRAY_TASK_ID} == 1 ]
then
    initpts=2
else
    initpts=$(expr ${SLURM_ARRAY_TASK_ID} \* 10 \- 15)
fi
sed -i "s/initpts.*/initpts 2 ${initpts}/" in_4D
last=$(sed -n '$=' 'in_4D')
sed -i -e $(expr ${initpts} \+ 16)','${last}'d' in_4D

./run_BOSS.sh
cd ..
