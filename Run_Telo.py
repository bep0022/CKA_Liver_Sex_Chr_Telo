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

import numpy as np
from pod5 import Reader


def pod5_to_signal_tsv(input_file, output_file):
    """
    Convert a POD5 file into a SquigglePull-style TSV signal file.

    This function reads raw nanopore signal data from a POD5 file,
    applies calibration to convert raw signals into picoamps, computes
    summary statistics, and writes the results to a TSV file.

    Args:
        input_file (str): Path to input POD5 file.
        output_file (str): Path to output TSV file.

    Returns:
        bool: True if processing succeeds, False if it fails.

    Raises:
        FileNotFoundError: If the input POD5 file does not exist.
        Exception: For any unexpected processing error.
    """
    try:
        with Reader(input_file) as reader, open(output_file, "w") as out:

            # Write header matching SquigglePull format
            out.write("read_id\tmean\tstdv\tstart\tlength\tsignal\n")

            for read in reader.reads():

                read_id = str(read.read_id)

                # Raw signal (int16 -> float32 for processing)
                raw_signal = np.array(read.signal, dtype=np.float32)

                # Calibration parameters
                offset = read.calibration.offset
                scale = read.calibration.range / read.calibration.digitisation

                # Convert to picoamps (SquigglePull-style normalization)
                signal_pa = (raw_signal + offset) * scale

                # Summary statistics
                mean = np.mean(signal_pa)
                stdv = np.std(signal_pa)
                start = 0
                length = len(signal_pa)

                # Convert full signal to TSV string
                signal_str = "\t".join(map(str, signal_pa))

                out.write(
                    f"{read_id}\t{mean}\t{stdv}\t{start}\t{length}\t{signal_str}\n"
                )

        return True

    except FileNotFoundError:
        print("Input POD5 file not found.")
        return False

    except Exception as e:
        print("Failed to process POD5 file.")
        print(f"Details: {e}")
        return False


def main():
    """
    Main entry point for POD5 signal extraction.

    Defines input/output paths, runs conversion,
    and prints status messages.
    """
    input_file = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Old/20250402_1036_MN39112_FBB00406_b8786f0b/pod5/FBB00406_b8786f0b_f9557bd8_0.pod5"
    output_file = "signal.tsv"

    print("DEBUG: starting POD5 processing")

    success = pod5_to_signal_tsv(input_file, output_file)

    if success:
        print("SquigglePull-style TSV created successfully.")
        print(f"Output: {output_file}")
    else:
        print("POD5 processing failed.")


if __name__ == "__main__":
    """
    Execute only when run directly.

    Prevents execution when imported as a module.
    """
    main()

##  OPTION 2 - IF CHOOSING SQUIGGLEPULL: .pod5 conversion to .fast5 for SquigglePull
#   Hashtag out if not choosing

import os
import subprocess


def convert_pod5_to_fast5(input_file, output_dir):
    """
    Convert a POD5 file to FAST5 format using the pod5 CLI.

    This function creates the output directory if it does not exist,
    then runs the `pod5 convert to_fast5` command via subprocess.

    Args:
        input_file (str): Path to the input POD5 file.
        output_dir (str): Directory where FAST5 files will be saved.

    Returns:
        bool: True if conversion succeeds, False if it fails.

    Raises:
        subprocess.CalledProcessError: If the subprocess fails and is not caught.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        subprocess.run(
            ["pod5", "convert", "to_fast5", input_file, "-o", output_dir],
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    """
    Main entry point for the script.

    Defines input and output paths, runs the conversion process,
    and prints the result to the console.
    """
    input_file = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Old/20250402_1036_MN39112_FBB00406_b8786f0b/pod5/FBB00406_b8786f0b_f9557bd8_0.pod5"
    output_dir = "output_fast5"

    print("DEBUG: about to run subprocess")

    success = convert_pod5_to_fast5(input_file, output_dir)

    if success:
        print(f"Conversion successful. Output in: {output_dir}")
    else:
        print("pod5 conversion failed.")


if __name__ == "__main__":
    """
    Execute the script only when run directly, not when imported.

    This ensures modularity by preventing automatic execution when
    the module is imported elsewhere.
    """
    main()

#   SquigglePull for input into TeloPeakCounter  
#   Alternative run option: python SquigglePull.py -rv -p input_dir -f all > signal.tsv

import os
import subprocess
from typing import Optional


def ensure_directory(path: str) -> None:
    """
    Ensure that a directory exists. If it does not exist, create it.

    Args:
        path (str): Path to the directory.
    """
    os.makedirs(path, exist_ok=True)


def run_squigglepull(
    script_path: str,
    input_dir: str,
    output_file: str
) -> subprocess.CompletedProcess:
    """
    Run the SquigglePull script using subprocess and capture its output.

    Args:
        script_path (str): Path to the SquigglePull.py script.
        input_dir (str): Directory containing input FAST5 files.
        output_file (str): File path to write stdout output.

    Returns:
        subprocess.CompletedProcess: The result object from subprocess.run().

    Raises:
        subprocess.CalledProcessError: If the subprocess exits with a non-zero status.
    """
    with open(output_file, "w") as outfile:
        result = subprocess.run(
            ["python", script_path, "-rv", "-p", input_dir],
            check=True,
            stdout=outfile,
            stderr=subprocess.PIPE,
            text=True
        )
    return result


def print_subprocess_result(result: subprocess.CompletedProcess) -> None:
    """
    Print the results of a completed subprocess execution.

    Args:
        result (subprocess.CompletedProcess): The completed subprocess result.
    """
    print("SquigglePull ran successfully!")
    print("Output saved to signal.tsv")

    if result.stderr:
        print("STDERR:\n", result.stderr)


def handle_subprocess_error(error: subprocess.CalledProcessError) -> None:
    """
    Handle errors raised during subprocess execution.

    Args:
        error (subprocess.CalledProcessError): The exception raised by subprocess.
    """
    print("SquigglePull failed.")
    print("Return code:", error.returncode)
    print("Error output:\n", error.stderr)


def main() -> None:
    """
    Main function to configure paths, run SquigglePull, and handle results.
    """
    squigglepull_path = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/SquiggleKit/SquigglePull.py"
    input_dir = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/output_fast5/"
    output_dir = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/signal_output/"
    output_file = "signal.tsv"

    ensure_directory(output_dir)

    try:
        result = run_squigglepull(
            script_path=squigglepull_path,
            input_dir=input_dir,
            output_file=output_file
        )
        print_subprocess_result(result)

    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e)


if __name__ == "__main__":
    main()

### Step 3. TeloPeakCounter

import subprocess


def run_telo_peak_counter(input_file, output_file, script_path):
    """
    Run the TeloPeakCounter.py script using subprocess.

    This function executes the external Python script with the provided
    input and output paths.

    Args:
        input_file (str): Path to the input TSV file.
        output_file (str): Path where results will be written.
        script_path (str): Path to the TeloPeakCounter.py script.

    Returns:
        bool: True if execution succeeds, False if it fails.

    Raises:
        subprocess.CalledProcessError: If the subprocess fails and is not caught.
    """
    try:
        subprocess.run(
            [
                "python3",
                script_path,
                "--input",
                input_file,
                "--output",
                output_file,
            ],
            check=True,
        )
        return True

    except subprocess.CalledProcessError:
        return False


def main():
    """
    Main entry point for the script.

    Defines input/output paths, runs TeloPeakCounter,
    and prints the result.
    """
    input_file = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/signal_output/signal.tsv"
    output_file = "/scratch/bep0022/CKA_Liver_Sex_Chr_Telo/signal_output/TeloPeak_results.txt"
    script_path = "/home/bep0022/2025_04_02_CKA_OLD_ChrSeq/CKA_Liver_Sex_Chr_Telo/TeloPeakCounter/TeloPeakCounter.py"

    print("DEBUG: about to run TeloPeakCounter subprocess")

    success = run_telo_peak_counter(input_file, output_file, script_path)

    if success:
        print(f"Output file created successfully: {output_file}")
    else:
        print("TeloPeakCounter.py failed.")


if __name__ == "__main__":
    """
    Execute the script only when run directly.

    Prevents execution when imported as a module.
    """
    main()
