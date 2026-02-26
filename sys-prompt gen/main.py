import argparse
import json
import os
import re
import sys
import requests
import pandas as pd
import urllib3
import urllib.request
import urllib.error

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# CONFIGURATION SECTION
# You can set these values here to run the script without command-line arguments.
# ==============================================================================
# Directory where CSV files are stored
CSV_FOLDER = "csv.files"

# Use raw string (r"...") for Windows paths to avoid escape character issues
# Just the filename, script will look in CSV_FOLDER
CSV_FILE_PATH = "ringcentral.com-organic.Positions-us-20260223-2026-02-24T17_21_16Z.csv"
ENDPOINT_URL = "https://n8n.crownitsolution.com/webhook/f33386cb-3518-4a91-b928-011a6de0589e"
OUTPUT_JSON_PATH = "output_new2.json"
# ==============================================================================

INSTRUCTIONS = (
    "You are an analysis agent that converts CSV content into a strict JSON file.\n"
    "Task:\n"
    "1) Read the provided CSV (first line is the header).\n"
    "2) Produce a JSON array; each element corresponds to a row in the CSV.\n"
    "3) Include exactly these keys for every object, in this order:\n"
    '   ["Keyword","Search Volume","Keyword Difficulty","CPC","URL","Position","Trends","Keyword Intents","SERP Features by Keyword"]\n'
    "4) Map values from columns with the exact same names. If a column is missing for a row, set its value to null.\n"
    "5) Preserve numeric types for numbers when unambiguous (e.g., Search Volume, Keyword Difficulty, CPC, Position). Otherwise leave as strings.\n"
    "6) For 'Keyword Intents' and 'SERP Features by Keyword', if the CSV cell contains multiple values separated by commas or semicolons, return an array of trimmed strings; otherwise return a single string as-is.\n"
    "7) Output only valid JSON with no markdown fencing, no comments, and no extra text.\n"
)

REQUIRED_COLUMNS = [
    "Keyword",
    "Search Volume",
    "Keyword Difficulty",
    "CPC",
    "URL",
    "Position",
    "Trends",
    "Keyword Intents",
    "SERP Features by Keyword",
]

def extract_json_from_text(text):
    if not text:
        raise ValueError("Response text is empty.")

    # 1. Try simple JSON load
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2. Try to find the largest outer block of JSON array or object
    candidates = []
    
    # Attempt to find JSON array [...]
    array_start = text.find('[')
    array_end = text.rfind(']')
    if array_start != -1 and array_end != -1 and array_end > array_start:
        candidates.append(text[array_start : array_end + 1])

    # Attempt to find JSON object {...}
    obj_start = text.find('{')
    obj_end = text.rfind('}')
    if obj_start != -1 and obj_end != -1 and obj_end > obj_start:
        candidates.append(text[obj_start : obj_end + 1])

    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            continue

    # 3. Fallback: regex search
    for m in re.finditer(r"\{.*\}|\[.*\]", text, flags=re.S):
        snippet = m.group(0)
        try:
            return json.loads(snippet)
        except Exception:
            pass

    raise ValueError("Response did not contain valid JSON.")

def normalize_label(s):
    return re.sub(r"\s+", " ", s.strip().lower())

def clean_csv_to_text(csv_path):
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    norm_to_canonical = {normalize_label(c): c for c in REQUIRED_COLUMNS}
    rename_map = {}
    for col in df.columns:
        n = normalize_label(col)
        if n in norm_to_canonical:
            rename_map[col] = norm_to_canonical[n]
    if rename_map:
        df = df.rename(columns=rename_map)
    for c in REQUIRED_COLUMNS:
        if c not in df.columns:
            df[c] = None
    df = df[REQUIRED_COLUMNS]
    for c in df.columns:
        df[c] = df[c].apply(lambda x: x if x is None else (x.strip() if isinstance(x, str) else x))
    for num_col in ["Search Volume", "Keyword Difficulty", "CPC", "Position"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
    df = df.dropna(how="all", subset=REQUIRED_COLUMNS)
    if "Keyword" in df.columns:
        df = df.drop_duplicates(subset=["Keyword"])
    
    # NOTE: Row limit removed to process full file
    # df = df.head(50) 
    
    return df.to_csv(index=False)

import math
import time

def main():
    print("Script starting...", flush=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=False, default=ENDPOINT_URL, help="POST webhook URL")
    parser.add_argument("--csv", required=False, default=CSV_FILE_PATH, help="Path to input CSV")
    parser.add_argument("--out", required=False, default=OUTPUT_JSON_PATH, help="Path to output JSON file")
    parser.add_argument("--timeout", type=int, default=120, help="Request timeout seconds")
    parser.add_argument("--batch-size", type=int, default=30, help="Number of rows per batch request")
    args = parser.parse_args()
    print(f"Args parsed. CSV: {args.csv}, Endpoint: {args.endpoint}, Out: {args.out}, Batch Size: {args.batch_size}", flush=True)

    # Check if we have a CSV path
    if not args.csv:
        print("Error: No CSV file provided.", file=sys.stderr)
        print("Please provide --csv argument OR set CSV_FILE_PATH in the script.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.csv):
        # Check if it exists in the CSV_FOLDER
        csv_in_folder = os.path.join(CSV_FOLDER, args.csv)
        if os.path.exists(csv_in_folder):
            print(f"Found CSV in {CSV_FOLDER}: {csv_in_folder}", flush=True)
            args.csv = csv_in_folder
        else:
            print("CSV file not found:", args.csv, file=sys.stderr)
            print(f"Also checked: {csv_in_folder}", file=sys.stderr)
            sys.exit(1)

    # 1. Load and clean the full dataframe first
    print("Loading and cleaning CSV...", flush=True)
    
    # We use the logic from clean_csv_to_text but adapt it to return a DataFrame
    # so we can slice it for batching.
    df = pd.read_csv(args.csv, dtype=str, keep_default_na=False)
    norm_to_canonical = {normalize_label(c): c for c in REQUIRED_COLUMNS}
    rename_map = {}
    for col in df.columns:
        n = normalize_label(col)
        if n in norm_to_canonical:
            rename_map[col] = norm_to_canonical[n]
    if rename_map:
        df = df.rename(columns=rename_map)
    for c in REQUIRED_COLUMNS:
        if c not in df.columns:
            df[c] = None
    df = df[REQUIRED_COLUMNS]
    for c in df.columns:
        df[c] = df[c].apply(lambda x: x if x is None else (x.strip() if isinstance(x, str) else x))
    for num_col in ["Search Volume", "Keyword Difficulty", "CPC", "Position"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
    df = df.dropna(how="all", subset=REQUIRED_COLUMNS)
    if "Keyword" in df.columns:
        df = df.drop_duplicates(subset=["Keyword"])
    
    total_rows = len(df)
    print(f"Total rows to process: {total_rows}", flush=True)
    
    all_results = []
    
    headers = {"Content-Type": "application/json"}

    # Load existing results if any, for resuming
    if os.path.exists(args.out):
        try:
            with open(args.out, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    all_results = json.loads(content)
                    print(f"Resuming from existing output file. Found {len(all_results)} items.", flush=True)
        except Exception as e:
            print(f"Error reading existing output file: {e}. Starting fresh.", file=sys.stderr)
            all_results = []

    start_row_index = len(all_results)
    if start_row_index >= total_rows:
        print("All rows appear to be processed already.", flush=True)
        return

    print(f"Starting processing from row {start_row_index}...", flush=True)
    
    df_remaining = df.iloc[start_row_index:]
    
    rows_to_process = len(df_remaining)
    num_batches = math.ceil(rows_to_process / args.batch_size)
    
    print(f"Remaining rows to process: {rows_to_process}. Batches: {num_batches}", flush=True)

    for i in range(num_batches):
        batch_start_rel = i * args.batch_size
        batch_end_rel = batch_start_rel + args.batch_size
        batch_df = df_remaining.iloc[batch_start_rel:batch_end_rel]
        
        current_batch_global_idx = start_row_index + batch_start_rel
        print(f"Processing batch {i+1}/{num_batches} (Global Row {current_batch_global_idx} to {current_batch_global_idx + len(batch_df)})...", flush=True)

        csv_text = batch_df.to_csv(index=False)
        
        message = (
            f"{INSTRUCTIONS}\n\n"
            "CSV:\n" + csv_text
        )

        payload = {
            "message": message
        }
        
        max_retries = 3
        batch_success = False
        
        for attempt in range(max_retries):
            try:
                json_str = json.dumps(payload)
                
                print(f"  Sending request for batch {i+1} (Attempt {attempt+1}/{max_retries})...", flush=True)
                # Use verify=False to avoid SSL issues
                resp = requests.post(args.endpoint, headers=headers, data=json_str, timeout=args.timeout, verify=False)
                
                print(f"  Response received for batch {i+1}. Status: {resp.status_code}", flush=True)
                
                if resp.status_code >= 400:
                    print(f"  Batch {i+1} failed: HTTP {resp.status_code}", file=sys.stderr)
                    if attempt < max_retries - 1:
                        time.sleep(2 * (attempt + 1))
                        continue
                    else:
                        break
                
                try:
                    data = resp.json()
                except Exception:
                    print(f"  Batch {i+1} received non-JSON response. Body: {resp.text[:200]}...", file=sys.stderr)
                    if attempt < max_retries - 1:
                        print(f"  Retrying batch {i+1}...", file=sys.stderr)
                        time.sleep(2 * (attempt + 1))
                        continue
                    else:
                        break

                output_text = None
                if isinstance(data, dict) and "output" in data and isinstance(data["output"], str):
                    output_text = data["output"]
                elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "output" in data[0] and isinstance(data[0]["output"], str):
                    output_text = data[0]["output"]
                elif isinstance(data, (dict, list)):
                    output_text = json.dumps(data)
                
                if output_text:
                    try:
                        batch_json = extract_json_from_text(output_text)
                        if isinstance(batch_json, list):
                            all_results.extend(batch_json)
                            print(f"  Batch {i+1} success. Extracted {len(batch_json)} items.", flush=True)
                            
                            # Save progress
                            with open(args.out, "w", encoding="utf-8") as f:
                                json.dump(all_results, f, ensure_ascii=False, indent=2)
                            
                            batch_success = True
                            break 
                        else:
                            print(f"  Batch {i+1} warning: Parsed JSON was not a list.", file=sys.stderr)
                    except Exception as e:
                        print(f"  Batch {i+1} JSON parse error: {e}", file=sys.stderr)
                else:
                     print(f"  Batch {i+1} warning: No output text found.", file=sys.stderr)
                
                if attempt < max_retries - 1:
                     print(f"  Retrying batch {i+1} due to extraction failure...", file=sys.stderr)
                     time.sleep(2 * (attempt + 1))
                     continue

            except Exception as e:
                print(f"  Batch {i+1} request exception: {e}", file=sys.stderr)
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
        
        if not batch_success:
            print(f"  Batch {i+1} failed permanently. Continuing to next batch, but data is missing.", file=sys.stderr)
            pass
            
        time.sleep(1)

    print(f"Finished processing. Total extracted items: {len(all_results)}", flush=True)
    print("Saved combined JSON to", args.out, flush=True)


if __name__ == "__main__":
    main()
