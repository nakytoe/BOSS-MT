#!/bin/bash

# load environment
export OMP_NUM_THREADS=1
export SLURM_MPI_TYPE=pmi2
module purge
module load openbabel/3.0.a1 intel/18.0.5 intel-mpi/18.0.5

### execute job (or any script)
export LC_ALL=en_US.utf8
cd exp_${SLURM_ARRAY_TASK_ID}
cwd=$(pwd)
cd /projappl/project_2000382/nuutti/BOSSMT
pipenv run ./run_boss.sh $cwd in_2D

