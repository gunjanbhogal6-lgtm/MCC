# Testing Guide for AutoSEO Dashboard

## Prerequisites

1. Python 3.9+ installed
2. Dependencies installed:
```bash
pip install -r requirements.txt
```

## Step 1: Start the Server

```bash
# Option A: Direct uvicorn
uvicorn api:app --host 0.0.0.0 --port 9100

# Option B: Using the start script
./start_server.sh
```

## Step 2: Access the Dashboard

| URL | Description |
|-----|-------------|
| http://localhost:9100/dashboard | Main Dashboard UI |
| http://localhost:9100/docs | FastAPI Documentation |
| http://localhost:9100/ | API Root |

## Step 3: Test Dashboard Features

### Tab 1: Upload & Preview

1. **Drag & Drop CSV Upload**
   - Use the sample file: `data/input/sample_keywords.csv`
   - Or upload your own keyword research CSV
   - Expected: Shows preview with opportunity scores

2. **Manual Keyword Input**
   - Enter a keyword manually with volume/difficulty
   - Click "Add Keyword"
   - Expected: Keyword appears in list

### Tab 2: Generate SEO

1. **Configure Settings**
   - Select target page: Home, Features, Pricing, etc.
   - Choose prompt template
   - Set max keywords (slider)

2. **Generate Preview**
   - Click "Generate Preview"
   - Expected: LLM generates SEO metadata

3. **Review Generated Content**
   - Check meta title (50-60 chars)
   - Check meta description (150-160 chars)
   - Review LSI keywords
   - Validate SEO score

### Tab 3: Compare & Edit

1. **View Side-by-Side**
   - Current SEO (from seo.json)
   - Generated SEO (proposed changes)

2. **Edit Content**
   - Modify generated content directly
   - Character counts update live

### Tab 4: Deploy

1. **Review Git Status**
   - Branch name
   - Files changed
   - Can deploy status

2. **Deploy Actions**
   - Add commit message
   - Commit only or Commit & Push

### Tab 5: Prompts

1. **Edit Prompt**
   - Modify the SEO prompt
   - Save for future use

2. **Use Templates**
   - World-Class SEO Master
   - E-Commerce SEO
   - Blog Content SEO
   - Local SEO

## API Testing

### Using curl

```bash
# Health check
curl http://localhost:9100/health

# Pipeline status
curl http://localhost:9100/pipeline/status

# Upload CSV
curl -X POST -F "file=@data/input/sample_keywords.csv" http://localhost:9100/dashboard/upload-preview

# Generate preview
curl -X POST http://localhost:9100/dashboard/generate-preview \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": [
      {"keyword": "AI business phone", "search_volume": 5000, "keyword_difficulty": 45, "cpc": 3.5, "position": 8, "url": "https://example.com", "intent": "commercial"}
    ]
  }'

# Validate SEO
curl -X POST http://localhost:9100/dashboard/validate-seo \
  -H "Content-Type: application/json" \
  -d '{
    "metaTitle": "AI Business Phone System | SalamTalk - 24/7 AI Receptionist",
    "metaDescription": "Get 24/7 AI receptionist for your business calls. SalamTalk handles customer inquiries, routes calls intelligently. Start free trial today.",
    "focusKeyword": "AI business phone system",
    "lsiKeywords": ["AI receptionist", "virtual phone", "call routing"]
  }'
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:9100"

# Get status
response = requests.get(f"{BASE_URL}/pipeline/status")
print(response.json())

# Upload CSV
with open("data/input/sample_keywords.csv", "rb") as f:
    response = requests.post(f"{BASE_URL}/dashboard/upload-preview", files={"file": f})
print(response.json())

# Generate preview
response = requests.post(
    f"{BASE_URL}/dashboard/generate-preview",
    json={
        "keywords": [
            {
                "keyword": "AI business phone",
                "search_volume": 5000,
                "keyword_difficulty": 45,
                "cpc": 3.5,
                "position": 8,
                "url": "https://example.com",
                "intent": "commercial"
            }
        ]
    }
)
print(response.json())
```

## Test Checklist

| Feature | Test | Expected Result |
|---------|------|-----------------|
| Dashboard loads | Open /dashboard | UI renders with 6 tabs |
| CSV upload | Upload sample_keywords.csv | Shows 15 keywords with scores |
| Manual input | Add keyword manually | Keyword appears in list |
| Generate preview | Click generate | SEO metadata generated |
| Character limits | Check title/description | Limits enforced (60/160) |
| SEO validation | Click validate | Shows score and grade |
| Comparison view | Check compare tab | Side-by-side view |
| Git status | Check deploy tab | Shows branch and changes |
| Prompts | Edit and save prompt | Saves to localStorage |
| API docs | Open /docs | Swagger UI loads |

## Troubleshooting

### Server won't start
```bash
# Check port is free
lsof -i :9100

# Kill existing process
kill -9 $(lsof -t -i:9100)
```

### LLM not responding
- Check `config.yaml` for correct LLM endpoint
- Verify n8n webhook is running
- Check `.env` for API keys

### CSV not parsing
- Ensure CSV has required columns
- Check encoding is UTF-8
- Verify column names match exactly

## Sample Files

- `data/input/sample_keywords.csv` - 15 sample keywords for testing
- `sites/salamtalk/src/data/seo.json` - Current SEO configuration
