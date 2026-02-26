#!/bin/bash
# Start AutoSEO Pipeline API Server

cd "$(dirname "$0")"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start server
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
