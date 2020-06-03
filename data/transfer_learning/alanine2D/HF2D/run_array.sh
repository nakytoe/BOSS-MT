#!/bin/bash
### run an array job of experiments

#BATCH --job-name=boss
#SBATCH --account=project_2000382
#SBATCH --array=1-20
#SBATCH --partition=small
#SBATCH --time=12:00:00
#SBATCH --ntasks=20
#SBATCH -o job/job%A_%a.out
#SBATCH -e job/job%A_%a.err
#####SBATCH --mem-per-cpu=2G

if [ ${SLURM_ARRAY_TASK_ID} != 0 ]
then
    scp -r exp_template exp_${SLURM_ARRAY_TASK_ID}
    cd exp_${SLURM_ARRAY_TASK_ID}
    initpts=$(expr ${SLURM_ARRAY_TASK_ID} \* 5)
    sed -i "s/initpts.*/initpts 5 ${initpts}/" in_2D
    sed -i -e "$(expr ${SLURM_ARRAY_TASK_ID} \* 5 \+ 20),124d;" in_2D
    cd ..
fi
./exp_${SLURM_ARRAY_TASK_ID}/run_BOSS.sh
