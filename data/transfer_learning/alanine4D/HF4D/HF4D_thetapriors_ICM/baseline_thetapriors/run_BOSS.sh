#!/bin/bash
#SBATCH --job-name=boss
#SBATCH --account=project_2000382
#SBATCH --partition=small
#SBATCH --time=04:00:00
#SBATCH --ntasks=20
#SBATCH -o job.out
#SBATCH -e job.err
#####SBATCH --mem-per-cpu=2G

# load environment
export OMP_NUM_THREADS=1
export SLURM_MPI_TYPE=pmi2
module purge
module load openbabel/3.0.a1 intel/18.0.5 intel-mpi/18.0.5

### execute job (or any script)
export LC_ALL=en_US.utf8
cwd=$(pwd)
cd /projappl/project_2000382/nuutti/BOSS
pipenv run ./run_boss.sh $cwd in_4D
