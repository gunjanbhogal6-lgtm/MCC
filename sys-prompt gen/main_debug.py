import argparse
import json
import os
import sys
import requests

ENDPOINT_URL = "https://n8n.crownitsolution.com/webhook/f33386cb-3518-4a91-b928-011a6de0589e"
CSV_FILE_PATH = "ringcentral.com-organic.Positions-us-20260223-2026-02-24T17_21_16Z.csv"
OUTPUT_JSON_PATH = "output_new.json"

def main():
    print("Script starting...", flush=True)
    # Simulate args
    args_endpoint = ENDPOINT_URL
    args_timeout = 120
    
    # Simulate cleaning
    print("Simulating CSV clean...", flush=True)
    csv_text = "Simulated CSV content" * 50 # Small content
    
    message = (
        "Instructions...\n\n"
        "CSV:\n" + csv_text
    )
    
    payload = {
        "message": message
    }
    
    headers = {"Content-Type": "application/json"}
    print("Sending POST request...", flush=True)
    try:
        print("Serializing JSON...", flush=True)
        json_payload = json.dumps(payload)
        print(f"Payload size: {len(json_payload)}", flush=True)
        resp = requests.post(args_endpoint, headers=headers, data=json_payload, timeout=args_timeout)
        print(f"Response received. Status: {resp.status_code}", flush=True)
    except Exception as e:
        print(f"Request failed with exception: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
