#!/usr/bin/bash
#SBATCH --job-name=EMc_l
#SBATCH --error=./logs/EMc_l_%a.err
#SBATCH --output=./logs/EMc_l_%a.out
#SBATCH --array=0-89
#SBATCH --time=48:00:00
#SBATCH -p normal
#SBATCH -c 8
#SBATCH --mem=32GB

ml python/3.12.1
time python3 ./sendOut.py 0 ${SLURM_ARRAY_TASK_ID} l