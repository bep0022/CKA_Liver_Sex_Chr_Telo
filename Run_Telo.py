#! /usr/bin/env python3

#### Scripting for Biologists
#### Making a high-throughput, reproducible workflow for quantifying telomeres from ONT sequencing data
### Steps:
### 1. TeloBP - identify subtelomere boundary and extract telomere reads
### 2. SquigglePull - extract raw signal data
### 3. TeloPeakCounter - measure telomeres

### TeloBP

### OPTION 1: Using .pod5 directly for .tsv output
# try/except = catches runtime errors you can’t fully predict (bad file format, read failure, permission issues, etc.)
# What to edit?

from pod5 import Reader

input_file = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Old/20250402_1036_MN39112_FBB00406_b8786f0b/pod5/FBB00406_b8786f0b_f9557bd8_25.pod5"
output_file = "signal.tsv"

try:
    with Reader(input_file) as reader, open(output_file, "w") as out:
        
        # Optional: header (some SquigglePull outputs include this, some don't)
        out.write("read_id\tsignal_length\tsignal\n")
        
        for read in reader.reads():
            read_id = str(read.read_id)
            signal = read.signal

            signal_length = len(signal)
            signal_str = "\t".join(map(str, signal))

            out.write(f"{read_id}\t{signal_length}\t{signal_str}\n")

    print("SquigglePull-style TSV created successfully.")
    print(f"Output: {output_file}")

except FileNotFoundError:
    print("Input POD5 file not found.")

except Exception as e:
    print("Failed to process POD5 file.")
    print(f"Details: {e}")

### OPTION 2, IF CHOOSING SQUIGGLEPULL: .pod5 conversion to .fast5 for SquigglePull
# bash code to convert to python: pod5 convert fast5 input.pod5 -o output_fast5/

### SquigglePull for input into TeloPeakCounter 
# bash code to convert to python: SquigglePull -i input.fast5/ -o signal.tsv 

#import subprocess

#subprocess.run(
#    ["SquigglePull","-i", "input.fast5","-o", "signal.tsv"]
#    check=True,
#    capture_output=True,
#    text=True
#)
#print("SquigglePull ran successfully!")
#print("Output saved to signal.tsv")

### TeloPeakCounter

#python3 TeloPeakCounter.py \
#    --input signal.tsv \
#    --output TeloPeak_results.txt
