import requests
import json

ENDPOINT_URL = "https://n8n.crownitsolution.com/webhook/f33386cb-3518-4a91-b928-011a6de0589e"
csv_text = "Simulated CSV content" * 2000
message = (
    "Instructions...\n\n"
    "CSV:\n" + csv_text
)
payload = {"message": message}
headers = {"Content-Type": "application/json"}

print("Sending POST...", flush=True)
try:
    print(f"Payload size: {len(json.dumps(payload))}", flush=True)
    resp = requests.post(ENDPOINT_URL, headers=headers, json=payload, timeout=30)
    print("Status:", resp.status_code, flush=True)
    print("Text:", resp.text[:100], flush=True)
except Exception as e:
    print("Error:", e, flush=True)
