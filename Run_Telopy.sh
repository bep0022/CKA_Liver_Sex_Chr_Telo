#! /bin/bash
#SBATCH --job-name=Test1_CKA_Run_Telopy            # job name
#SBATCH --nodes=1                                    # node(s) required for job
#SBATCH --ntasks=1                                   # number of tasks across all nodes
#SBATCH --partition=general                          # name of partition
#SBATCH --time=24:00:00                              # Run time (D-HH:MM:SS)
#SBATCH --output=test1-%j.out                        # Output file. %j is replaced with job ID
#SBATCH --error=test1_error-%j.err                   # Error file. %j is replaced with job ID
#SBATCH --mail-type=ALL                              # will send email for begin,end,fail
#SBATCH --mail-user=bep0022@auburn.edu               # CHANGE THIS EMAIL ADDRESS WITH YOUR EMAIL ADDRESS

##This script employs Easley through Auburn University; to run this script, use "sbatch [script]"
##see https://hpc.auburn.edu/hpc/docs/hpcdocs/build/html/easley/easley.html for more information

##########  Define variables and make directories

WD=/scratch/bep0022/CKA_Liver_Sex_Chr_Telo

mkdir -p $WD
cd $WD

python3 /home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/Run_Telo.py
