# Scripting for biologists project

For the first chapter of my dissertation, I have obtained Nanopore sequencing data from old (5 years) male and female brown anole lizards. I selectively sequenced their sex chromosomes with the goal of quantifying the telomere lengths on the X and Y chromosomes.
In this class, my goal is to adapt packages (TeloPeakCounter and TeloBP/TeloNP) produced by the Greider Lab and published in [Karimian et al. 2024](https://doi.org/10.1126/science.ado0431) to quantify the telomere sequences in my own data. Specifically, TeloBP is available as command line one liners and I want to combine them into a more high-throughout python script that would be compatible with running on the HPC Easley.    

## Sex chromosome telomere sequencing analysis
## Steps:
1.   TeloBP - identify subtelomere boundary and extract telomere reads
2.   SquigglePull - extract raw signal data
3.   TeloPeakCounter - measure telomeres from signal data

## Start by cloning the repository, which contains all other relevant repositories!

```
git clone git@github.com:bep0022/CKA_Liver_Sex_Chr_Telo.git
```
## Scripts:

[Run_Telo.py](https://github.com/bep0022/CKA_Liver_Sex_Chr_Telo/blob/master/Run_Telo.py):
-   A python script with modularized steps for SquigglePull and TeloPeakCounter
[Run_Telosh.py](https://github.com/bep0022/CKA_Liver_Sex_Chr_Telo/blob/master/Run_Telopy.sh):
-   A shell script that allows the modules to be submitted as a job on a HPC
-   One liners for TeloBP/TeloNP

### TeloBP/TeloNP

Determination of the subtelomere boundary to begin the calculation of the telomere length.

```
python3 teloBPBedGenome.py /path/to/input/genomic.fna /path/to/output/output.bed
python3 teloBPCmd.py /path/to/input/fastq/ /path/to/output/ --fileMode --teloNP -v --save_graphs
```

Inputs:

-   The reference genome file (.fa, .fna, .fasta)
-   The basecalled sequence files (.fastq)

Outputs:

-   teloBPBedGenome.py - output a .bed file containing telomere boundary coordinates from a reference genome
-   teloBPCmd.py - output a .csv file containing read names and telomere lengths

### SquigglePull

Extract the signal data drom the raw electrical signal. 
SquigglePull is solely compatible with the older ONT .fast5 raw data format. 
If you have .fast5 files then no conversion is necessary and you can jump to SquigglePull module. 
If you have the newer .pod5 raw data file format, follow either option 1 where python directly extracts a SquigglePull style .tsv from your .pod5 or option 2 that first does a .pod5 to .fast5 conversion for SquigglePull compatibility. 
Hashtag out or remove the options not followed in Run_Telo.py

Input:
-   Raw Nanopore sequencing data file (.fast5 or .pod5)

Output:
-   File containing the read_id, start/end sites, signal or list of raw current values, length, mean, and stdv (.tsv)

### TeloPeakCounter

Peak calling of raw signal data to measure telomere length.

Input:

-   The extracted signal data from Nanopore sequencing data files (.tsv)

Output:

-   The count of the number of peaks in the telomeric region (.txt)

### Here's a list of links to the GreiderLab's original resources:

-   [TeloPeakCounter Repo](https://github.com/GreiderLab/TeloPeakCounter/tree/master)
-   [TeloBP/TeloNP Repo](https://github.com/GreiderLab/TeloBP)

### Here's a link to SquigglePull's original resource:

-   [SquigglePull Repo](https://github.com/Psy-Fer/SquiggleKit)
