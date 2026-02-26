FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY pipeline/ ./pipeline/
COPY sites/ ./sites/
COPY data/ ./data/
COPY config.yaml .
COPY api.py .
COPY run.py .

# Create necessary directories
RUN mkdir -p data/input data/processed data/cache data/backups logs

# Expose port 9100 (Coolify uses 8000)
EXPOSE 9100

# Start server on port 9100
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "9100"]
