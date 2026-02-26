import subprocess
import os
import sys

# ==============================================================================
# CONFIGURATION SECTION
# List your CSV files here. They must be located in the 'csv.files' folder.
# Example: "my_file.csv", "another_file.csv"
# ==============================================================================

CSV_FILES_TO_PROCESS = [
    "dialpad.com-organic.Positions-us-20260223-2026-02-24T22_57_03Z.csv",
    # Add more files here...
    # "another_csv_file.csv",
]

# ==============================================================================

def run_conversion():
    print("Starting batch conversion process...", flush=True)
    print(f"Found {len(CSV_FILES_TO_PROCESS)} files to process.", flush=True)

    for i, csv_filename in enumerate(CSV_FILES_TO_PROCESS):
        print(f"\n[{i+1}/{len(CSV_FILES_TO_PROCESS)}] Processing: {csv_filename}", flush=True)
        
        # Generate output filename: replace .csv with .json
        base_name = os.path.splitext(csv_filename)[0]
        output_filename = f"{base_name}.json"
        
        # Construct the command
        # python main.py --csv "filename.csv" --out "filename.json"
        command = [
            sys.executable,  # Uses the current python interpreter
            "main.py",
            "--csv", csv_filename,
            "--out", output_filename
        ]
        
        try:
            # Run the command and wait for it to finish
            # check=True raises CalledProcessError if the command fails
            subprocess.run(command, check=True)
            print(f"Successfully processed {csv_filename} -> {output_filename}", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {csv_filename}. Command failed with exit code {e.returncode}", flush=True)
        except Exception as e:
            print(f"Unexpected error for {csv_filename}: {e}", flush=True)

    print("\nAll tasks completed.", flush=True)

if __name__ == "__main__":
    run_conversion()
