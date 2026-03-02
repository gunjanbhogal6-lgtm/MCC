#!/bin/bash
#
# AutoSEO Automation Script
# Handles server startup, pipeline execution, and git conflicts
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PORT=${PORT:-9100}
HOST=${HOST:-0.0.0.0}
VENV_PATH="venv"
LOG_FILE="logs/auto_pipeline.log"

# Functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
    mkdir -p logs
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARNING] $1" >> "$LOG_FILE"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        log_error "Virtual environment not found at $VENV_PATH"
        log "Creating virtual environment..."
        python3 -m venv "$VENV_PATH"
        source "$VENV_PATH/bin/activate"
        pip install -r requirements.txt
    fi
}

# Activate virtual environment
activate_venv() {
    log "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
}

# Check if server is running
is_server_running() {
    curl -s "http://localhost:$PORT/health" > /dev/null 2>&1
}

# Start server
start_server() {
    if is_server_running; then
        log "Server already running on port $PORT"
        return 0
    fi
    
    log "Starting server on port $PORT..."
    
    # Kill any existing process on the port
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    
    # Start server in background
    nohup uvicorn api:app --host $HOST --port $PORT > logs/server.log 2>&1 &
    
    # Wait for server to start
    for i in {1..30}; do
        if is_server_running; then
            log_success "Server started successfully"
            return 0
        fi
        sleep 1
    done
    
    log_error "Failed to start server"
    return 1
}

# Check for CSV files
check_csv_files() {
    CSV_COUNT=$(find data/input -name "*.csv" -type f 2>/dev/null | wc -l)
    echo "$CSV_COUNT"
}

# Run pipeline
run_pipeline() {
    log "Running pipeline..."
    
    CSV_COUNT=$(check_csv_files)
    
    if [ "$CSV_COUNT" -eq 0 ]; then
        log_warning "No CSV files found in data/input/"
        return 1
    fi
    
    log "Found $CSV_COUNT CSV file(s)"
    
    # Run pipeline via API
    RESPONSE=$(curl -s -X POST "http://localhost:$PORT/pipeline/run" \
        -H "Content-Type: application/json" \
        -d '{"force_push": true}')
    
    SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))" 2>/dev/null || echo "false")
    
    if [ "$SUCCESS" = "True" ]; then
        log_success "Pipeline completed successfully"
        echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
        return 0
    else
        log_error "Pipeline failed"
        echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
        return 1
    fi
}

# Upload CSV
upload_csv() {
    local csv_file="$1"
    
    if [ ! -f "$csv_file" ]; then
        log_error "CSV file not found: $csv_file"
        return 1
    fi
    
    log "Uploading CSV: $csv_file"
    
    # Copy to input directory
    cp "$csv_file" data/input/
    
    log_success "CSV uploaded to data/input/"
}

# Watch mode
watch_mode() {
    log "Starting watch mode..."
    log "Monitoring data/input/ for new CSV files..."
    
    while true; do
        CSV_COUNT=$(check_csv_files)
        
        if [ "$CSV_COUNT" -gt 0 ]; then
            log "Processing $CSV_COUNT CSV file(s)..."
            run_pipeline
        fi
        
        sleep 60
    done
}

# Handle git conflicts
handle_git_conflicts() {
    log "Checking for git conflicts..."
    
    # Fetch remote
    git fetch origin 2>/dev/null || true
    
    # Check if we're behind
    LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "")
    REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "")
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        log_warning "Remote has new commits - will use force push"
    fi
}

# Main
main() {
    echo ""
    echo "=========================================="
    echo "  AutoSEO Pipeline Automation"
    echo "=========================================="
    echo ""
    
    # Check and activate venv
    check_venv
    activate_venv
    
    # Handle command
    case "${1:-start}" in
        start)
            start_server
            log_success "Dashboard available at: http://localhost:$PORT/dashboard"
            log_success "API docs available at: http://localhost:$PORT/docs"
            ;;
        stop)
            log "Stopping server..."
            lsof -ti$PORT | xargs kill -9 2>/dev/null || true
            log_success "Server stopped"
            ;;
        restart)
            $0 stop
            sleep 2
            $0 start
            ;;
        run)
            start_server
            run_pipeline
            ;;
        upload)
            if [ -z "$2" ]; then
                log_error "Usage: $0 upload <csv_file>"
                exit 1
            fi
            start_server
            upload_csv "$2"
            run_pipeline
            ;;
        watch)
            start_server
            watch_mode
            ;;
        status)
            if is_server_running; then
                log_success "Server is running on port $PORT"
                curl -s "http://localhost:$PORT/pipeline/status" | python3 -m json.tool
            else
                log_error "Server is not running"
            fi
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|run|upload|watch|status}"
            echo ""
            echo "Commands:"
            echo "  start     Start the API server"
            echo "  stop      Stop the API server"
            echo "  restart   Restart the API server"
            echo "  run       Run the pipeline once"
            echo "  upload    Upload a CSV and run pipeline"
            echo "  watch     Watch for new CSV files and auto-run"
            echo "  status    Check server and pipeline status"
            exit 1
            ;;
    esac
}

main "$@"
