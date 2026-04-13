#! /bin/bash
#SBATCH --job-name=Test38_CKA_Run_Telopy            # job name
#SBATCH --nodes=1                                    # node(s) required for job
#SBATCH --ntasks=1                                   # number of tasks across all nodes
#SBATCH --partition=general                          # name of partition
#SBATCH --time=24:00:00                              # Run time (D-HH:MM:SS)
#SBATCH --output=test38-%j.out                        # Output file. %j is replaced with job ID
#SBATCH --error=test38_error-%j.err                   # Error file. %j is replaced with job ID
#SBATCH --mail-type=ALL                              # will send email for begin,end,fail
#SBATCH --mail-user=bep0022@auburn.edu               # CHANGE THIS EMAIL ADDRESS WITH YOUR EMAIL ADDRESS

##This script employs Easley through Auburn University; to run this script, use "sbatch [script]"
##see https://hpc.auburn.edu/hpc/docs/hpcdocs/build/html/easley/easley.html for more information

########## Load modules

module load python/3.10
pip install --user pod5 numpy

##########  Define variables and make directories

WD=/scratch/bep0022/CKA_Liver_Sex_Chr_Telo

mkdir -p $WD
cd $WD

# Find the telomere/subtelomere boundary positions from the reference genome
python3 /home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/TeloBP/Scripts/teloBPBedGenome.py /home/bep0022/ReferenceGenomes/rAnoSag1.mat/ncbi_dataset/data/GCF_037176765.1/GCF_037176765.1_rAnoSag1.mat_genomic.fna output.bed

# Calculate telomere lengths
python3 /home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/TeloBP/Scripts/teloBPCmd.py /home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Old/20250402_1036_MN39112_FBB00406_b8786f0b/fastq_pass/barcode01/ /scratch/bep0022/CKA_Liver_Sex_Chr_Telo/ --fileMode --teloNP -v --save_graphs

# Run script for SquigglePull and TeloPeakCounter
python3 /home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/Run_Telo.py
