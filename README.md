# Scripting for biologists project

For the first chapter of my dissertation, I have obtained Nanopore sequencing data from old (5 years) male and female brown anole lizards. I selectively sequenced their sex chromosomes with the goal of quantifying the telomere lengths on the X and Y chromosomes.
In this class, my goal is to adapt packages (TeloPeakCounter and TeloBP/TeloNP) produced by the Greider Lab [Karimian et al. 2024](https://doi.org/10.1126/science.ado0431) to quantify the telomere sequences in my own data. Specifically, TeloBP is available as command line one liners and I want to combine them into a more high-throughout python script.    

## Sex chromosome telomere sequencing analysis

### TeloPeakCounter

Peak calling of raw electrical data to measure telomere length.

Input:

-   The raw Nanopore sequencing data files (fast5 or pod5)

Steps:

-   Extract using SquigglePull
-   Use getTeloCountLengthFromSignal() function to get the telomere length of the sample 

### TeloBP/TeloNP

Determination of the subtelomere boundary to begin the calculation of the telomere length. 

Input:

- The basecalled sequence files (fastq)   

Steps:

-   teloBPCmd.py - output a .csv file containing read names and telomere lengths
-   trimGenome.py - output a .bed file of a genome sequence with telomeres trimmed off
-   teloBPBedGenome.py - output a .bed file containing telomere boundary coordinates from a reference genome
-   getTeloBoundary() - returns the distance between the telomere boundary and the end of the telomere sequence

### Here's a list of links to the GreiderLab's original resources:

-   [TeloPeakCounter](https://github.com/GreiderLab/TeloPeakCounter/tree/master)
-   [TeloBP/TeloNP](https://github.com/GreiderLab/TeloBP)
