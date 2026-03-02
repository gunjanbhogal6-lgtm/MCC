# AutoSEO Dashboard

A comprehensive web-based dashboard for managing the AutoSEO Pipeline.

## Features

### 1. Upload & Preview Tab
- Drag & drop CSV file upload
- Real-time data preview with validation
- Keyword opportunity scoring
- Manual keyword input
- Quick wins, high-value, and low-hanging fruit identification

### 2. Generate SEO Tab
- Configure generation settings
- Select target page type
- Choose prompt template
- Preview SEO content before saving
- Run full pipeline or individual stages

### 3. Compare & Edit Tab
- Side-by-side comparison of current vs proposed SEO
- Edit generated content directly
- Character count validation
- Apply changes selectively

### 4. Deploy Tab
- Git status overview
- Commit message customization
- Commit only or commit & push
- Deployment history

### 5. Prompts Tab
- Prompt editor with syntax highlighting
- Pre-built templates:
  - World-Class SEO Master (recommended)
  - E-Commerce SEO
  - Blog Content SEO
  - Local SEO
- Custom prompt support

### 6. Settings Tab
- Pipeline configuration display
- Environment variables
- API endpoint settings

## API Endpoints

### Dashboard Endpoints (`/dashboard/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/dashboard/upload-preview` | Upload CSV and get preview |
| POST | `/dashboard/generate-preview` | Generate SEO preview without saving |
| GET | `/dashboard/deploy-preview` | Preview changes before deploying |
| GET | `/dashboard/prompts` | Get available prompt templates |
| GET | `/dashboard/seo-comparison` | Compare current vs generated SEO |
| GET | `/dashboard/history` | Get pipeline execution history |
| POST | `/dashboard/validate-seo` | Validate SEO content |

### Pipeline Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pipeline/status` | Get pipeline status |
| POST | `/pipeline/run` | Run full pipeline |
| POST | `/pipeline/ingest` | Run ingest stage only |
| POST | `/pipeline/generate` | Run generate stage only |
| POST | `/pipeline/transform` | Run transform stage only |
| POST | `/pipeline/deploy` | Run deploy stage only |
| POST | `/upload` | Upload CSV file |
| GET | `/seo/current` | Get current seo.json |

## Quick Start

```bash
# Start the API server
uvicorn api:app --host 0.0.0.0 --port 9100

# Open dashboard in browser
open http://localhost:9100/dashboard
```

## Structured LLM Response Format

The dashboard expects LLM responses in this format:

```json
{
  "metaTitle": "Primary Keyword | Brand Name - Value Proposition",
  "metaDescription": "Action-oriented description with CTA. 150-160 characters.",
  "h1Tag": "Main heading with primary keyword",
  "focusKeyword": "primary-keyword",
  "secondaryKeywords": ["keyword 1", "keyword 2", "keyword 3"],
  "lsiKeywords": ["semantic keyword 1", "semantic keyword 2", "...15-20 keywords"],
  "primaryKeywords": ["high opportunity keyword 1", "...10-15 keywords"],
  "longTailKeywords": ["long tail variation 1", "...5-8 keywords"],
  "targetAudience": "Specific buyer persona description",
  "searchIntent": "informational|commercial|transactional|navigational",
  "pageGoal": "ToFu|MoFu|BoFu",
  "contentStrategy": "Brief content approach description",
  "competitorSentence": "Unique differentiation statement",
  "schemaType": "SoftwareApplication|Product|Service|Article|FAQ",
  "internalLinks": ["suggested link 1", "suggested link 2"],
  "ctaPhrase": "Primary call-to-action"
}
```

## Keyword Input Format

```json
{
  "keyword": "target keyword phrase",
  "search_volume": 5000,
  "keyword_difficulty": 45,
  "cpc": 2.50,
  "position": 12,
  "url": "https://example.com/page",
  "intent": "informational"
}
```

## CSV Requirements

Required columns:
- Keyword
- Search Volume
- Keyword Difficulty
- CPC
- Position
- URL
- Trends
- Keyword Intents
- SERP Features by Keyword

## Character Limits

| Field | Min | Max | Optimal |
|-------|-----|-----|---------|
| Meta Title | 50 | 60 | 55-60 |
| Meta Description | 150 | 160 | 155-160 |
| H1 Tag | - | 70 | 50-70 |
| LSI Keywords | 15 | 20 | 18-20 |
| Primary Keywords | 10 | 15 | 12-15 |

## Opportunity Scoring

Keywords are scored using:
```
opportunity_score = (search_volume * (100 - keyword_difficulty)) / 100
```

Categories:
- **Quick Wins**: Position 4-15, Volume ≥500
- **High Value**: Volume ≥1000, Difficulty ≤70, CPC >$1
- **Low Hanging Fruit**: Position ≤10, Volume ≥100
