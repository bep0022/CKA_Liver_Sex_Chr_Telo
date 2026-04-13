#! /usr/bin/env python3

#### Scripting for Biologists
#### Making a high-throughput, reproducible workflow for quantifying telomeres from ONT sequencing data
### Steps:
### 1. TeloBP - identify subtelomere boundary and extract telomere reads
### 2. SquigglePull - extract raw signal data
### 3. TeloPeakCounter - measure telomeres

### Step 1. TeloBP
#   Submitted as job in sh script prior to running Run_Telo.py

### Step 2. SquigglePull

##  OPTION 1 - SquigglePull Alternative: Using .pod5 directly for .tsv output
#   Hashtag out if not choosing
#   What to edit? input_file variable

from pod5 import Reader
import numpy as np

input_file = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Old/20250402_1036_MN39112_FBB00406_b8786f0b/pod5/FBB00406_b8786f0b_f9557bd8_0.pod5"
output_file = "signal.tsv"

try:
    with Reader(input_file) as reader, open(output_file, "w") as out:

        # Match SquigglePull column structure
        out.write("read_id\tmean\tstdv\tstart\tlength\tsignal\n")

        for read in reader.reads():
            read_id = str(read.read_id)

            # Raw signal (int16)
            raw_signal = np.array(read.signal, dtype=np.float32)

            # Calibration parameters
            offset = read.calibration.offset
            scale = read.calibration.range / read.calibration.digitisation

            # Convert to picoamps (this is the critical SquigglePull step)
            signal_pa = (raw_signal + offset) * scale

            # Stats on scaled signal (NOT raw)
            mean = np.mean(signal_pa)
            stdv = np.std(signal_pa)
            start = 0
            length = len(signal_pa)

            signal_str = "\t".join(map(str, signal_pa))

            out.write(f"{read_id}\t{mean}\t{stdv}\t{start}\t{length}\t{signal_str}\n")

    print("SquigglePull-style TSV created successfully.")
    print(f"Output: {output_file}")

except FileNotFoundError:
    print("Input POD5 file not found.")

except Exception as e:
    print("Failed to process POD5 file.")
    print(f"Details: {e}")

##  OPTION 2 - IF CHOOSING SQUIGGLEPULL: .pod5 conversion to .fast5 for SquigglePull
#   Hashtag out if not choosing

import os
import subprocess

input_file = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Old/20250402_1036_MN39112_FBB00406_b8786f0b/pod5/FBB00406_b8786f0b_f9557bd8_0.pod5"
output_dir = "output_fast5"

print("DEBUG: about to run subprocess")

os.makedirs(output_dir, exist_ok=True)

try:
    subprocess.run(
        ["pod5", "convert", "to_fast5", input_file, "-o", output_dir],
        check=True
    )
    print(f"Conversion successful. Output in: {output_dir}")

except subprocess.CalledProcessError:
    print("pod5 conversion failed.")

#   SquigglePull for input into TeloPeakCounter  
#   Alternative run option: python SquigglePull.py -rv -p input_dir -f all > signal.tsv
import subprocess
import os

squigglepull_path = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/SquiggleKit/SquigglePull.py"
input_dir = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/output_fast5/"
output_dir = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/signal_output/"
os.makedirs(output_dir, exist_ok=True)

import subprocess

try:
    with open("signal.tsv", "w") as outfile:
        result = subprocess.run(
            ["python", squigglepull_path, "-rv", "-p", input_dir],
            check=True,
            stdout=outfile,
            stderr=subprocess.PIPE,
            text=True
        )

    print("SquigglePull ran successfully!")
    print("Output saved to signal.tsv")

    if result.stderr:
        print("STDERR:\n", result.stderr)

except subprocess.CalledProcessError as e:
    print("SquigglePull failed.")
    print("Return code:", e.returncode)
    print("Error output:\n", e.stderr)

### Step 3. TeloPeakCounter

import subprocess

input_file = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/signal_output/signal.tsv"
output_file = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/signal_output/TeloPeak_results.txt"
script_path = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/TeloPeakCounter/TeloPeakCounter.py"

try:
    subprocess.run(
        ["python3", script_path, "--input", input_file, "--output", output_file],
        check=True
    )
    print(f"Output file created successfully: {output_file}")

except subprocess.CalledProcessError:
    print("TeloPeakCounter.py failed.")
