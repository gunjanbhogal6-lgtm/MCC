import requests
print("Testing connection...")
try:
    resp = requests.get("https://n8n.crownitsolution.com/webhook/f33386cb-3518-4a91-b928-011a6de0589e", timeout=10)
    print("Status:", resp.status_code)
    print("Text:", resp.text[:100])
except Exception as e:
    print("Error:", e)
