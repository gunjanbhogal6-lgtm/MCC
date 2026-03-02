"""
FastAPI Backend Server for AutoSEO Pipeline

Endpoints:
- POST /pipeline/run        - Run full pipeline
- POST /pipeline/ingest     - Run ingest stage
- POST /pipeline/generate   - Run generate stage
- POST /pipeline/transform  - Run transform stage
- POST /pipeline/deploy     - Run deploy stage
- GET  /pipeline/status     - Get pipeline status
- POST /upload              - Upload CSV file
- GET  /dashboard           - Dashboard UI
"""

import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pipeline import Pipeline
from pipeline.stages.deploy import DeployResult
from pipeline.stages.generate import GenerateResult
from pipeline.stages.ingest import IngestResult
from pipeline.stages.transform import TransformResult
from pipeline.utils.config import get_config
from dashboard_api import router as dashboard_router

app = FastAPI(
    title="AutoSEO Pipeline API",
    description="Backend API for automated SEO content generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)

pipeline = Pipeline()
config = get_config()

last_run_result = None


class PipelineRequest(BaseModel):
    max_keywords: Optional[int] = None
    dry_run: bool = False
    no_deploy: bool = False
    input_file: Optional[str] = None


class StageRequest(BaseModel):
    input_file: Optional[str] = None
    max_keywords: Optional[int] = None
    dry_run: bool = False


class PipelineResponse(BaseModel):
    success: bool
    message: str
    timestamp: str
    details: Optional[dict] = None


def result_to_dict(result) -> dict:
    """Convert stage result to dictionary"""
    if isinstance(result, IngestResult):
        return {
            "stage": "ingest",
            "success": result.success,
            "keywords_processed": result.total_keywords,
            "files_processed": len(result.processed_files),
            "errors": result.errors
        }
    elif isinstance(result, GenerateResult):
        return {
            "stage": "generate",
            "success": result.success,
            "batches_processed": f"{result.successful_batches}/{result.total_batches}",
            "errors": result.errors
        }
    elif isinstance(result, TransformResult):
        return {
            "stage": "transform",
            "success": result.success,
            "changes": result.changes,
            "backup_path": result.backup_path,
            "errors": result.errors
        }
    elif isinstance(result, DeployResult):
        return {
            "stage": "deploy",
            "success": result.success,
            "committed": result.committed,
            "pushed": result.pushed,
            "commit_hash": result.commit_hash,
            "errors": result.errors
        }
    return {"success": result.success if hasattr(result, 'success') else True}


@app.get("/")
async def root():
    return {
        "name": "AutoSEO Pipeline API",
        "version": "1.0.0",
        "status": "running",
        "dashboard": "/dashboard",
        "docs": "/docs"
    }


@app.get("/pipeline/status")
async def get_status():
    """Get current pipeline status"""
    status = pipeline.get_status()
    
    input_files = []
    input_dir = Path(config.input_dir)
    if input_dir.exists():
        input_files = [f.name for f in input_dir.glob("*.csv")]
    
    return {
        "status": "ready",
        "config": {
            "input_directory": config.input_dir,
            "seo_json_path": config.seo_json_path,
            "max_keywords": config.get('input', 'max_keywords', default=100),
            "batch_size": config.batch_size
        },
        "git": status.get('git_status', {}),
        "input_files": input_files,
        "last_run": last_run_result
    }


@app.post("/pipeline/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    """Run the complete pipeline"""
    global last_run_result
    
    try:
        result = pipeline.run(
            input_csv=request.input_file,
            max_keywords=request.max_keywords,
            dry_run=request.dry_run,
            no_deploy=request.no_deploy
        )
        
        last_run_result = {
            "timestamp": datetime.now().isoformat(),
            "success": result.success,
            "summary": result.summary,
            "errors": result.errors
        }
        
        return PipelineResponse(
            success=result.success,
            message="Pipeline completed successfully" if result.success else "Pipeline failed",
            timestamp=datetime.now().isoformat(),
            details=result.summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pipeline/ingest", response_model=PipelineResponse)
async def run_ingest(request: StageRequest):
    """Run only the ingest stage"""
    try:
        result = pipeline.run_ingest_only(
            input_csv=request.input_file,
            max_keywords=request.max_keywords
        )
        
        return PipelineResponse(
            success=result.success,
            message=f"Ingested {result.total_keywords} keywords" if result.success else "Ingest failed",
            timestamp=datetime.now().isoformat(),
            details=result_to_dict(result)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pipeline/generate", response_model=PipelineResponse)
async def run_generate():
    """Run only the generate stage"""
    try:
        result = pipeline.run_generate_only()
        
        return PipelineResponse(
            success=result.success,
            message=f"Generated content from {result.successful_batches}/{result.total_batches} batches" if result.success else "Generation failed",
            timestamp=datetime.now().isoformat(),
            details=result_to_dict(result)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pipeline/transform", response_model=PipelineResponse)
async def run_transform():
    """Run only the transform stage"""
    try:
        result = pipeline.run_transform_only()
        
        return PipelineResponse(
            success=result.success,
            message=f"Updated seo.json with {len(result.changes)} changes" if result.success else "Transform failed",
            timestamp=datetime.now().isoformat(),
            details=result_to_dict(result)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pipeline/deploy", response_model=PipelineResponse)
async def run_deploy(request: StageRequest):
    """Run only the deploy stage"""
    try:
        result = pipeline.run_deploy_only(dry_run=request.dry_run)
        
        return PipelineResponse(
            success=result.success,
            message=f"Committed and pushed: {result.commit_hash}" if result.success else "Deploy failed",
            timestamp=datetime.now().isoformat(),
            details=result_to_dict(result)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file to the input directory"""
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    input_dir = Path(config.input_dir)
    input_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = input_dir / file.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "success": True,
        "message": f"Uploaded {file.filename}",
        "path": str(file_path)
    }


@app.get("/seo/current")
async def get_current_seo():
    """Get current seo.json content"""
    seo_path = Path(config.seo_json_path)
    
    if not seo_path.exists():
        raise HTTPException(status_code=404, detail="seo.json not found")
    
    import json
    with open(seo_path, 'r') as f:
        return json.load(f)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the dashboard UI"""
    dashboard_path = Path(__file__).parent / "dashboard" / "index.html"
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
