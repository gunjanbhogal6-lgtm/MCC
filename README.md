# AutoSEO Pipeline

Automated SEO content generation pipeline that processes keyword research data and generates optimized SEO metadata for websites.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR SERVER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────┐     ┌─────────────────────────────┐  │
│   │   Pipeline API      │     │   Frontend (Coolify)        │  │
│   │   Backend Service   │     │   - salamtalk Astro site    │  │
│   │   Port: 8000        │     │   - Auto-deploys on push    │  │
│   │                     │     │                             │  │
│   │   POST /pipeline/run│────▶│   sites/salamtalk/          │  │
│   │                     │     │   src/data/seo.json         │  │
│   └─────────────────────┘     └─────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: CLI (Manual)

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python run.py

# Run with specific CSV file
python run.py --input data/input/keywords.csv

# Dry run (preview without deploying)
python run.py --dry-run
```

### Option 2: API Server (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
./start_server.sh
# or
uvicorn api:app --host 0.0.0.0 --port 8000

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/pipeline/status` | Get pipeline status |
| POST | `/pipeline/run` | Run full pipeline |
| POST | `/pipeline/ingest` | Run ingest stage only |
| POST | `/pipeline/generate` | Run generate stage only |
| POST | `/pipeline/transform` | Run transform stage only |
| POST | `/pipeline/deploy` | Run deploy stage only |
| POST | `/upload` | Upload CSV file |
| GET | `/seo/current` | Get current seo.json |

### Example API Calls

```bash
# Get status
curl http://localhost:8000/pipeline/status

# Run full pipeline
curl -X POST http://localhost:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"max_keywords": 50, "no_deploy": false}'

# Upload CSV and run
curl -X POST http://localhost:8000/upload \
  -F "file=@keywords.csv"

# Run pipeline with uploaded file
curl -X POST http://localhost:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"input_file": "keywords.csv", "max_keywords": 100}'
```

## Deployment Options

### Docker

```bash
# Build and run with Docker
docker build -t autoseo-api .
docker run -p 8000:8000 -v $(pwd)/data:/app/data autoseo-api

# Or with docker-compose
docker-compose up -d
```

### Coolify / Docker Compose

The included `docker-compose.yml` is ready for Coolify deployment.

## CLI Commands

```bash
python run.py                          # Full pipeline
python run.py --stage ingest           # Run specific stage
python run.py --input keywords.csv     # Process specific file
python run.py --max-keywords 50        # Limit keywords
python run.py --dry-run                # Preview without changes
python run.py --no-deploy              # Skip git push
python run.py --status                 # Show pipeline status
python run.py --json                   # JSON output
python run.py -v                       # Verbose output
```

## Architecture

```
AutoSEO/
├── pipeline/
│   ├── stages/
│   │   ├── ingest.py      # CSV processing & validation
│   │   ├── generate.py    # LLM content generation
│   │   ├── transform.py   # Merge into seo.json
│   │   └── deploy.py      # Git commit & push
│   ├── utils/
│   │   ├── csv_parser.py  # CSV handling
│   │   ├── json_handler.py
│   │   ├── llm_client.py  # n8n webhook client
│   │   ├── git_manager.py
│   │   └── logger.py
│   ├── schemas/
│   └── main.py            # Pipeline orchestrator
├── sites/
│   └── salamtalk/         # Target website
│       └── src/data/seo.json
├── data/
│   ├── input/             # Drop CSV files here
│   ├── processed/         # Archived CSVs
│   └── cache/             # Intermediate data
├── config.yaml            # Pipeline configuration
└── run.py                 # CLI entry point
```

## Pipeline Stages

### Stage 1: Ingest
- Scans `data/input/` for CSV files
- Validates required columns
- Calculates opportunity scores
- Archives processed files

### Stage 2: Generate
- Batches keyword data
- Sends to n8n LLM webhook
- Generates:
  - Meta title (≤60 chars)
  - Meta description (≤160 chars)
  - Focus keyword
  - LSI keywords
  - Target audience

### Stage 3: Transform
- Loads existing `seo.json`
- Incrementally merges new content
- Preserves existing sections
- Creates backup before update

### Stage 4: Deploy
- Checks git status
- Auto-commits changes
- Pushes to configured branch
- Returns commit hash

## Configuration

Edit `config.yaml`:

```yaml
input:
  directory: "data/input"
  max_keywords: 100

llm:
  endpoint: "https://n8n.example.com/webhook/xxx"
  batch_size: 30
  max_retries: 3

output:
  seo_json_path: "sites/salamtalk/src/data/seo.json"

git:
  auto_commit: true
  auto_push: true
  branch: "main"
```

## CLI Commands

```bash
python run.py                          # Full pipeline
python run.py --stage ingest           # Run specific stage
python run.py --input keywords.csv     # Process specific file
python run.py --max-keywords 50        # Limit keywords
python run.py --dry-run                # Preview without changes
python run.py --no-deploy              # Skip git push
python run.py --status                 # Show pipeline status
python run.py --json                   # JSON output
python run.py -v                       # Verbose output
```

## Input CSV Format

Expected columns:
- `Keyword` - Target keyword
- `Search Volume` - Monthly searches
- `Keyword Difficulty` - 0-100 score
- `CPC` - Cost per click
- `Position` - Current ranking
- `URL` - Ranking page
- `Trends` - Trend data
- `Keyword Intents` - Search intents
- `SERP Features by Keyword` - SERP features

## Output (seo.json)

```json
{
  "site": { "name": "...", "url": "..." },
  "seo": {
    "metaTitle": "...",
    "metaDescription": "...",
    "focusKeyword": "...",
    "lsiKeywords": [...],
    "primaryKeywords": [...]
  },
  "keywords": {
    "primary": [...],
    "secondary": [...]
  },
  "sections": { ... }
}
```

## CI/CD Integration

When deployed, the pipeline:
1. Updates `seo.json`
2. Commits changes to main branch
3. Pushes to remote
4. Triggers Coolify deployment

## Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=pipeline
```
