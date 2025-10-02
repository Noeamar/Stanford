#!/usr/bin/bash
#SBATCH --job-name=EMs_e
#SBATCH --error=./logs/EMs_e.err
#SBATCH --output=./logs/EMs_e.out
#SBATCH --time=48:00:00
#SBATCH -p normal
#SBATCH -c 8
#SBATCH --mem=8GB

ml python/3.12.1
time python3 ./sendOut.py 1