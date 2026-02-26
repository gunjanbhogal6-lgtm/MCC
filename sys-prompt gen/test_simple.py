import time
import sys
import requests

print("Start test", flush=True)
try:
    print("Requesting google...", flush=True)
    r = requests.get("https://google.com", timeout=5)
    print(f"Google status: {r.status_code}", flush=True)
except Exception as e:
    print(f"Google error: {e}", flush=True)

print("Requesting n8n...", flush=True)
try:
    r = requests.post("https://n8n.crownitsolution.com/webhook/f33386cb-3518-4a91-b928-011a6de0589e", json={"message": "test"}, timeout=10, verify=False)
    print(f"n8n status: {r.status_code}", flush=True)
    print(f"n8n text: {r.text[:100]}", flush=True)
except Exception as e:
    print(f"n8n error: {e}", flush=True)

print("End test", flush=True)
