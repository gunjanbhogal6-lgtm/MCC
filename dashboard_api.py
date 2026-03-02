"""
Dashboard API - Extended endpoints for SEO Pipeline Dashboard
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from pipeline import Pipeline
from pipeline.prompts.seo_prompts import SEO_MASTER_PROMPT, validate_seo_content
from pipeline.utils.config import get_config
from pipeline.utils.llm_client import LLMClient
from pipeline.utils.json_handler import extract_json_from_text

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

pipeline = Pipeline()
config = get_config()


class KeywordInput(BaseModel):
    keyword: str
    search_volume: int = 0
    keyword_difficulty: int = 0
    cpc: float = 0.0
    position: int = 0
    url: str = ""
    intent: str = "informational"


class GeneratePreviewRequest(BaseModel):
    keywords: List[KeywordInput]
    custom_prompt: Optional[str] = None
    target_page: Optional[str] = "home"


class SEOMetadataResponse(BaseModel):
    metaTitle: str = Field(..., max_length=60)
    metaDescription: str = Field(..., max_length=160)
    h1Tag: str = Field(..., max_length=70)
    focusKeyword: str
    secondaryKeywords: List[str] = Field(default_factory=list)
    lsiKeywords: List[str] = Field(default_factory=list)
    primaryKeywords: List[str] = Field(default_factory=list)
    longTailKeywords: List[str] = Field(default_factory=list)
    targetAudience: str
    searchIntent: str
    pageGoal: str
    contentStrategy: str
    competitorSentence: str
    schemaType: str
    internalLinks: List[str] = Field(default_factory=list)
    ctaPhrase: str


class KeywordAnalysisResponse(BaseModel):
    keyword: str
    volume: int
    difficulty: int
    opportunity_score: float
    intent: str
    cpc: float
    position: int
    url: str
    recommendation: str


class PreviewResponse(BaseModel):
    success: bool
    seo_metadata: Optional[SEOMetadataResponse] = None
    keyword_analysis: List[KeywordAnalysisResponse] = []
    raw_llm_response: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
    timestamp: str


class CSVPreviewResponse(BaseModel):
    success: bool
    filename: str
    total_rows: int
    columns: List[str]
    keywords: List[Dict[str, Any]]
    validation_errors: List[str] = Field(default_factory=list)
    opportunity_summary: Dict[str, Any] = Field(default_factory=dict)


class ChangeSetItem(BaseModel):
    field: str
    old_value: Any
    new_value: Any
    impact: str
    recommendation: str


class DeployPreviewResponse(BaseModel):
    success: bool
    current_seo: Dict[str, Any]
    proposed_changes: List[ChangeSetItem]
    files_to_commit: List[str]
    branch: str
    can_deploy: bool
    warnings: List[str] = Field(default_factory=list)


@router.post("/upload-preview", response_model=CSVPreviewResponse)
async def upload_and_preview_csv(file: UploadFile = File(...)):
    """Upload CSV and get a preview of the data with analysis"""
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    import pandas as pd
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        df = pd.read_csv(tmp_path, dtype=str, keep_default_na=False)
        
        df.columns = df.columns.str.strip()
        
        os.unlink(tmp_path)
        
        columns = list(df.columns)
        validation_errors = []
        
        if 'Keyword' not in columns:
            validation_errors.append("Missing required column: Keyword")
        
        keywords = []
        opportunity_summary = {
            "total_volume": 0,
            "total_traffic": 0,
            "total_traffic_cost": 0,
            "avg_difficulty": 0.0,
            "avg_position": 0.0,
            "quick_wins": 0,
            "high_value": 0,
            "low_hanging_fruit": 0,
            "top_positions": 0
        }
        
        if 'Keyword' in df.columns:
            for idx, row in df.head(100).iterrows():
                kw_value = row.get('Keyword', '')
                if not kw_value or pd.isna(kw_value):
                    continue
                    
                try:
                    keyword_data = {
                        "keyword": str(kw_value),
                        "search_volume": int(float(row.get('Search Volume', 0) or 0)),
                        "keyword_difficulty": int(float(row.get('Keyword Difficulty', 0) or 0)),
                        "cpc": float(row.get('CPC', 0) or 0),
                        "position": int(float(row.get('Position', 0) or 0)),
                        "url": str(row.get('URL', '')),
                        "intent": str(row.get('Keyword Intents', 'informational')),
                        "trends": str(row.get('Trends', '')),
                        "serp_features": str(row.get('SERP Features by Keyword', '')),
                        "traffic": int(float(row.get('Traffic', 0) or 0)),
                        "traffic_cost": float(row.get('Traffic Cost', 0) or 0),
                        "competition": float(row.get('Competition', 0) or 0),
                        "position_type": str(row.get('Position Type', 'Organic'))
                    }
                except (ValueError, TypeError) as e:
                    continue
                
                volume = keyword_data['search_volume']
                difficulty = keyword_data['keyword_difficulty']
                position = keyword_data['position']
                
                opportunity_score = (volume * (100 - min(difficulty, 99))) / 100 if volume > 0 else 0
                keyword_data['opportunity_score'] = round(opportunity_score, 2)
                
                keywords.append(keyword_data)
                
                opportunity_summary["total_volume"] += volume
                opportunity_summary["total_traffic"] += keyword_data['traffic']
                opportunity_summary["total_traffic_cost"] += keyword_data['traffic_cost']
                
                if position == 1:
                    opportunity_summary["top_positions"] += 1
                if 4 <= position <= 15 and volume >= 500:
                    opportunity_summary["quick_wins"] += 1
                if volume >= 1000 and difficulty <= 70:
                    opportunity_summary["high_value"] += 1
                if position <= 10 and volume >= 100:
                    opportunity_summary["low_hanging_fruit"] += 1
            
            if keywords:
                avg_diff = sum(k['keyword_difficulty'] for k in keywords) / len(keywords)
                avg_pos = sum(k['position'] for k in keywords) / len(keywords)
                opportunity_summary["avg_difficulty"] = round(avg_diff, 1)
                opportunity_summary["avg_position"] = round(avg_pos, 1)
        
        keywords.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
        
        return CSVPreviewResponse(
            success=len(validation_errors) == 0,
            filename=file.filename or "unknown.csv",
            total_rows=len(df),
            columns=columns,
            keywords=keywords[:25],
            validation_errors=validation_errors,
            opportunity_summary=opportunity_summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@router.post("/generate-preview", response_model=PreviewResponse)
async def generate_seo_preview(request: GeneratePreviewRequest):
    """Generate SEO metadata preview without saving"""
    try:
        if not request.keywords:
            return PreviewResponse(
                success=False,
                errors=["No keywords provided"],
                timestamp=datetime.now().isoformat()
            )
        
        import pandas as pd
        
        keywords_data = []
        for kw in request.keywords[:30]:
            keywords_data.append({
                "Keyword": kw.keyword,
                "Search Volume": kw.search_volume,
                "Keyword Difficulty": kw.keyword_difficulty,
                "CPC": kw.cpc,
                "Position": kw.position,
                "URL": kw.url,
                "Trends": "",
                "Keyword Intents": kw.intent,
                "SERP Features by Keyword": ""
            })
        
        df = pd.DataFrame(keywords_data)
        csv_text = df.to_csv(index=False)
        
        system_prompt = request.custom_prompt or SEO_MASTER_PROMPT
        
        llm_client = LLMClient(
            endpoint=config.llm_endpoint,
            timeout=config.timeout,
            max_retries=config.max_retries,
            batch_size=config.batch_size
        )
        
        llm_result = llm_client.generate(csv_text, system_prompt)
        
        if not llm_result.get("success"):
            return PreviewResponse(
                success=False,
                errors=[f"LLM error: {llm_result.get('error', 'Unknown error')}"],
                timestamp=datetime.now().isoformat()
            )
        
        raw_response = llm_result.get("response", "")
        
        parsed = extract_json_from_text(raw_response)
        
        if not parsed:
            return PreviewResponse(
                success=False,
                raw_llm_response=raw_response,
                errors=["Could not parse JSON from LLM response"],
                timestamp=datetime.now().isoformat()
            )
        
        if isinstance(parsed, list):
            parsed = parsed[0] if parsed else {}
        
        validated = validate_seo_content(parsed)
        
        seo_metadata = SEOMetadataResponse(
            metaTitle=validated.get("metaTitle", "")[:60],
            metaDescription=validated.get("metaDescription", "")[:160],
            h1Tag=validated.get("h1Tag", "")[:70],
            focusKeyword=validated.get("focusKeyword", ""),
            secondaryKeywords=validated.get("secondaryKeywords", [])[:5],
            lsiKeywords=validated.get("lsiKeywords", [])[:20],
            primaryKeywords=validated.get("primaryKeywords", [])[:15],
            longTailKeywords=validated.get("longTailKeywords", [])[:8],
            targetAudience=validated.get("targetAudience", ""),
            searchIntent=validated.get("searchIntent", "commercial"),
            pageGoal=validated.get("pageGoal", "MoFu"),
            contentStrategy=validated.get("contentStrategy", ""),
            competitorSentence=validated.get("competitorSentence", ""),
            schemaType=validated.get("schemaType", "SoftwareApplication"),
            internalLinks=validated.get("internalLinks", [])[:5],
            ctaPhrase=validated.get("ctaPhrase", "Start Free Trial")
        )
        
        keyword_analysis = []
        for kw in request.keywords:
            volume = kw.search_volume
            difficulty = kw.keyword_difficulty
            opportunity = (volume * (100 - min(difficulty, 99))) / 100 if volume > 0 else 0
            
            recommendation = _get_keyword_recommendation(kw.position, volume, difficulty)
            
            keyword_analysis.append(KeywordAnalysisResponse(
                keyword=kw.keyword,
                volume=volume,
                difficulty=difficulty,
                opportunity_score=round(opportunity, 2),
                intent=kw.intent,
                cpc=kw.cpc,
                position=kw.position,
                url=kw.url,
                recommendation=recommendation
            ))
        
        keyword_analysis.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        return PreviewResponse(
            success=True,
            seo_metadata=seo_metadata,
            keyword_analysis=keyword_analysis[:15],
            raw_llm_response=raw_response if len(raw_response) < 5000 else raw_response[:5000] + "...",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating preview: {str(e)}")


@router.get("/deploy-preview", response_model=DeployPreviewResponse)
async def get_deploy_preview():
    """Preview what will change before deploying"""
    try:
        seo_path = Path(config.seo_json_path)
        
        if not seo_path.exists():
            return DeployPreviewResponse(
                success=False,
                current_seo={},
                proposed_changes=[],
                files_to_commit=[],
                branch="main",
                can_deploy=False,
                warnings=["seo.json not found"]
            )
        
        with open(seo_path, 'r') as f:
            current_seo = json.load(f)
        
        cache_file = Path(config.cache_dir) / "generated_content.json"
        proposed_seo = None
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                proposed_seo = json.load(f)
        
        proposed_changes = []
        
        if proposed_seo:
            current_seo_section = current_seo.get("seo", {})
            
            if proposed_seo.get("metaTitle") and proposed_seo["metaTitle"] != current_seo_section.get("metaTitle"):
                proposed_changes.append(ChangeSetItem(
                    field="metaTitle",
                    old_value=current_seo_section.get("metaTitle", ""),
                    new_value=proposed_seo["metaTitle"],
                    impact="high",
                    recommendation="Meta title is critical for search rankings"
                ))
            
            if proposed_seo.get("metaDescription") and proposed_seo["metaDescription"] != current_seo_section.get("metaDescription"):
                proposed_changes.append(ChangeSetItem(
                    field="metaDescription",
                    old_value=current_seo_section.get("metaDescription", "")[:100] + "...",
                    new_value=proposed_seo["metaDescription"],
                    impact="medium",
                    recommendation="Meta description affects click-through rates"
                ))
            
            if proposed_seo.get("focusKeyword") and proposed_seo["focusKeyword"] != current_seo_section.get("focusKeyword"):
                proposed_changes.append(ChangeSetItem(
                    field="focusKeyword",
                    old_value=current_seo_section.get("focusKeyword", ""),
                    new_value=proposed_seo["focusKeyword"],
                    impact="high",
                    recommendation="Focus keyword drives content optimization"
                ))
            
            current_lsi = set(current_seo_section.get("lsiKeywords", []))
            new_lsi = set(proposed_seo.get("lsiKeywords", []))
            added_lsi = new_lsi - current_lsi
            
            if added_lsi:
                proposed_changes.append(ChangeSetItem(
                    field="lsiKeywords",
                    old_value=f"{len(current_lsi)} keywords",
                    new_value=f"{len(current_lsi | added_lsi)} keywords (+{len(added_lsi)} new)",
                    impact="medium",
                    recommendation=f"Adding {len(added_lsi)} new LSI keywords for semantic SEO"
                ))
        
        git_status = pipeline.get_status().get('git_status', {})
        
        files_to_commit = []
        if git_status.get('has_changes'):
            files_to_commit = git_status.get('modified_files', [])
        
        warnings = []
        if len(proposed_changes) == 0:
            warnings.append("No changes detected - nothing to deploy")
        
        return DeployPreviewResponse(
            success=True,
            current_seo=current_seo.get("seo", {}),
            proposed_changes=proposed_changes,
            files_to_commit=files_to_commit,
            branch=git_status.get('branch', 'main'),
            can_deploy=len(proposed_changes) > 0,
            warnings=warnings
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating deploy preview: {str(e)}")


@router.get("/prompts")
async def get_available_prompts():
    """Get available SEO prompt templates"""
    return {
        "prompts": [
            {
                "id": "default",
                "name": "World-Class SEO Master Prompt",
                "description": "Comprehensive SEO prompt optimized for 2024-2025 best practices",
                "preview": SEO_MASTER_PROMPT[:500] + "...",
                "target": "all"
            },
            {
                "id": "ecommerce",
                "name": "E-Commerce SEO Prompt",
                "description": "Optimized for product pages and e-commerce sites",
                "preview": "Optimized for product pages...",
                "target": "product"
            },
            {
                "id": "blog",
                "name": "Blog Content SEO Prompt",
                "description": "Optimized for blog posts and articles",
                "preview": "Optimized for blog content...",
                "target": "article"
            },
            {
                "id": "local",
                "name": "Local SEO Prompt",
                "description": "Optimized for local business pages",
                "preview": "Optimized for local SEO...",
                "target": "local"
            }
        ],
        "custom_prompt_support": True
    }


@router.get("/seo-comparison")
async def get_seo_comparison():
    """Compare current vs generated SEO content"""
    seo_path = Path(config.seo_json_path)
    cache_file = Path(config.cache_dir) / "generated_content.json"
    
    current = None
    generated = None
    
    if seo_path.exists():
        with open(seo_path, 'r') as f:
            data = json.load(f)
            current = data.get("seo", {})
    
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            generated = json.load(f)
    
    return {
        "current": current,
        "generated": generated,
        "has_changes": current != generated if current and generated else False
    }


@router.get("/history")
async def get_pipeline_history(limit: int = 10):
    """Get recent pipeline execution history"""
    logs_dir = Path(config.get('logging', 'directory', default='logs'))
    
    history = []
    
    if logs_dir.exists():
        log_files = sorted(logs_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        for log_file in log_files[:limit]:
            try:
                stat = log_file.stat()
                history.append({
                    "file": log_file.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception:
                pass
    
    return {
        "history": history,
        "total": len(history)
    }


def _get_keyword_recommendation(position: int, volume: int, difficulty: int) -> str:
    """Generate recommendation for a keyword"""
    if position <= 3:
        return "Excellent ranking! Monitor and maintain position."
    elif position <= 10:
        if volume >= 1000:
            return "Quick win opportunity - optimize to reach top 3"
        else:
            return "Good position - maintain current optimization"
    elif position <= 20:
        if difficulty <= 40:
            return "High opportunity - low difficulty, good for content creation"
        else:
            return "Medium opportunity - consider building authority first"
    elif position <= 50:
        if volume >= 500:
            return "Potential opportunity - needs content investment"
        else:
            return "Low priority - limited traffic potential"
    else:
        if difficulty <= 30 and volume >= 1000:
            return "Hidden opportunity - low competition, high volume"
        else:
            return "Low priority - consider long-tail variations"


@router.post("/validate-seo")
async def validate_seo_content_endpoint(content: Dict[str, Any]):
    """Validate SEO content against best practices"""
    errors = []
    warnings = []
    suggestions = []
    
    meta_title = content.get("metaTitle", "")
    if len(meta_title) == 0:
        errors.append("Meta title is empty")
    elif len(meta_title) < 50:
        warnings.append(f"Meta title is short ({len(meta_title)} chars) - optimal is 50-60")
    elif len(meta_title) > 60:
        errors.append(f"Meta title is too long ({len(meta_title)} chars) - max is 60")
    
    meta_desc = content.get("metaDescription", "")
    if len(meta_desc) == 0:
        errors.append("Meta description is empty")
    elif len(meta_desc) < 150:
        warnings.append(f"Meta description is short ({len(meta_desc)} chars) - optimal is 150-160")
    elif len(meta_desc) > 160:
        errors.append(f"Meta description is too long ({len(meta_desc)} chars) - max is 160")
    else:
        suggestions.append("Meta description length is optimal")
    
    if not content.get("focusKeyword"):
        warnings.append("No focus keyword specified")
    
    lsi_keywords = content.get("lsiKeywords", [])
    if len(lsi_keywords) < 10:
        suggestions.append(f"Consider adding more LSI keywords (currently {len(lsi_keywords)})")
    elif len(lsi_keywords) >= 15:
        suggestions.append("Good number of LSI keywords for semantic SEO")
    
    primary_keywords = content.get("primaryKeywords", [])
    if len(primary_keywords) < 5:
        suggestions.append(f"Consider adding more primary keywords (currently {len(primary_keywords)})")
    
    score = 100
    score -= len(errors) * 20
    score -= len(warnings) * 10
    score = max(0, score)
    
    return {
        "valid": len(errors) == 0,
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F",
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
        "character_counts": {
            "metaTitle": len(meta_title),
            "metaDescription": len(meta_desc)
        }
    }
