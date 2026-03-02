# AutoSEO Pipeline

Automated SEO content generation pipeline that processes keyword research data and generates optimized SEO metadata for websites.

## Project Structure

```
AutoSEO/
├── pipeline/                # Backend SEO pipeline
│   ├── stages/              # Pipeline stages (ingest, generate, transform, deploy)
│   ├── utils/               # Utilities (CSV parser, LLM client, git manager)
│   └── main.py              # Pipeline orchestrator
├── sites/
│   └── salamtalk/           # SalamTalk frontend (Astro)
│       ├── src/             # Source files
│       ├── Dockerfile       # Frontend Docker config
│       └── nginx.conf       # Nginx configuration
├── data/
│   ├── input/               # Drop CSV files here
│   ├── processed/           # Archived CSVs
│   └── cache/               # Intermediate data
├── api.py                   # FastAPI backend server
├── run.py                   # CLI entry point
├── config.yaml              # Pipeline configuration
└── docker-compose.yml       # Docker compose for deployment
```

## Two Deployments

This project deploys as **two separate services** in Coolify:

| Service | Directory | Port | Description |
|---------|-----------|------|-------------|
| autoseo-api | Root (`/`) | 9100 | FastAPI backend |
| salamtalk | `sites/salamtalk/` | 80 | Astro frontend |

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend development)
- Docker (for deployment)

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run pipeline
python run.py

# Or start API server
uvicorn api:app --host 0.0.0.0 --port 9100
```

### Frontend Setup

```bash
cd sites/salamtalk

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build
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

## CLI Commands

```bash
python run.py                    # Full pipeline
python run.py --stage ingest     # Run specific stage
python run.py --input file.csv   # Process specific file
python run.py --max-keywords 50  # Limit keywords
python run.py --dry-run          # Preview without changes
python run.py --no-deploy        # Skip git push
python run.py --status           # Show pipeline status
```

## Pipeline Stages

1. **Ingest** - Process CSV files, validate columns, calculate opportunity scores
2. **Generate** - Send data to LLM webhook, generate SEO metadata
3. **Transform** - Merge generated content into seo.json
4. **Deploy** - Git commit and push changes

## Configuration

Edit `config.yaml`:

```yaml
llm:
  endpoint: "https://n8n.example.com/webhook/xxx"
  batch_size: 30

output:
  seo_json_path: "sites/salamtalk/src/data/seo.json"

git:
  auto_commit: true
  auto_push: true
  branch: "main"
```

## Input CSV Format

Required columns:
- `Keyword` - Target keyword
- `Search Volume` - Monthly searches
- `Keyword Difficulty` - 0-100 score
- `CPC` - Cost per click
- `Position` - Current ranking
- `URL` - Ranking page
- `Trends` - Trend data
- `Keyword Intents` - Search intents
- `SERP Features by Keyword` - SERP features

## Deployment (Coolify)

### Backend (autoseo-api)

1. Build Pack: `Dockerfile`
2. Port Exposes: `9100`
3. Watch Paths (optional):
   ```
   pipeline/**
   api.py
   config.yaml
   requirements.txt
   Dockerfile
   ```

### Frontend (salamtalk)

1. Build Pack: `Dockerfile`
2. Base Directory: `sites/salamtalk`
3. Dockerfile Location: `Dockerfile`
4. Port Exposes: `80`
5. Watch Paths (optional):
   ```
   sites/salamtalk/**
   ```

## Testing

```bash
pytest tests/
pytest tests/ --cov=pipeline
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `pytest tests/`
4. Submit a pull request

## License

MIT


```bash
export VERTEX_ACCESS_TOKEN=$(gcloud auth print-access-token)
opencode
```