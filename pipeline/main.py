"""
Main Pipeline Orchestrator - Coordinates all stages
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .stages.deploy import DeployStage, DeployResult
from .stages.generate import GenerateStage, GenerateResult
from .stages.ingest import IngestStage, IngestResult
from .stages.transform import TransformStage, TransformResult
from .utils.config import Config, get_config, reload_config
from .utils.logger import get_logger


@dataclass
class PipelineResult:
    """Complete pipeline execution result"""
    success: bool
    started_at: str = ""
    finished_at: str = ""
    duration_seconds: float = 0.0
    
    ingest: Optional[IngestResult] = None
    generate: Optional[GenerateResult] = None
    transform: Optional[TransformResult] = None
    deploy: Optional[DeployResult] = None
    
    errors: List[str] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class Pipeline:
    """
    AutoSEO Pipeline Orchestrator
    
    Coordinates the execution of all stages:
    1. Ingest - Process CSV input files
    2. Generate - LLM-powered content generation
    3. Transform - Merge into seo.json
    4. Deploy - Git commit and push
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the pipeline.
        
        Args:
            config_path: Optional path to config.yaml
        """
        if config_path:
            reload_config(config_path)
        
        self.config = get_config()
        self.logger = get_logger()
        
        self._ingest_stage = IngestStage()
        self._generate_stage = GenerateStage()
        self._transform_stage = TransformStage()
        self._deploy_stage = DeployStage()
    
    def run(
        self,
        input_csv: Optional[str] = None,
        max_keywords: Optional[int] = None,
        skip_stages: Optional[List[str]] = None,
        dry_run: bool = False,
        no_deploy: bool = False
    ) -> PipelineResult:
        """
        Run the complete pipeline.
        
        Args:
            input_csv: Optional specific CSV file to process
            max_keywords: Maximum keywords to process
            skip_stages: List of stage names to skip
            dry_run: If True, don't make actual changes
            no_deploy: If True, skip the deploy stage
            
        Returns:
            PipelineResult with complete execution details
        """
        skip_stages = skip_stages or []
        start_time = datetime.now()
        
        result = PipelineResult(
            success=False,
            started_at=start_time.isoformat()
        )
        
        self.logger.info("=" * 60)
        self.logger.info("AutoSEO Pipeline Starting")
        self.logger.info("=" * 60)
        
        try:
            # Stage 1: Ingest
            if "ingest" not in skip_stages:
                ingest_result = self._ingest_stage.run(
                    input_path=input_csv,
                    max_keywords=max_keywords
                )
                result.ingest = ingest_result
                
                if not ingest_result.success:
                    result.errors.append("Ingest stage failed")
                    return result
            else:
                self.logger.info("Skipping ingest stage")
            
            # Stage 2: Generate
            if "generate" not in skip_stages:
                generate_result = self._generate_stage.run(
                    ingested_data_path=result.ingest.data_path if result.ingest else None
                )
                result.generate = generate_result
                
                if not generate_result.success:
                    result.errors.append("Generate stage failed")
                    return result
            else:
                self.logger.info("Skipping generate stage")
            
            # Stage 3: Transform
            if "transform" not in skip_stages:
                transform_result = self._transform_stage.run(
                    generated_content=result.generate.generated_content if result.generate else None
                )
                result.transform = transform_result
                
                if not transform_result.success:
                    result.errors.append("Transform stage failed")
                    return result
            else:
                self.logger.info("Skipping transform stage")
            
            # Stage 4: Deploy
            if not no_deploy and "deploy" not in skip_stages and not dry_run:
                deploy_result = self._deploy_stage.run()
                result.deploy = deploy_result
                
                if not deploy_result.success:
                    result.errors.append("Deploy stage failed")
                    return result
            else:
                self.logger.info("Skipping deploy stage")
            
            result.success = True
            
        except Exception as e:
            result.errors.append(f"Pipeline error: {str(e)}")
            self.logger.error(f"Pipeline failed: {e}")
        
        end_time = datetime.now()
        result.finished_at = end_time.isoformat()
        result.duration_seconds = (end_time - start_time).total_seconds()
        
        # Build summary
        result.summary = self._build_summary(result)
        
        self.logger.info("=" * 60)
        self.logger.info("Pipeline Complete")
        self.logger.info(f"Duration: {result.duration_seconds:.2f}s")
        self.logger.info(f"Success: {result.success}")
        self.logger.info("=" * 60)
        
        return result
    
    def run_ingest_only(
        self,
        input_csv: Optional[str] = None,
        max_keywords: Optional[int] = None
    ) -> IngestResult:
        """Run only the ingest stage"""
        return self._ingest_stage.run(input_path=input_csv, max_keywords=max_keywords)
    
    def run_generate_only(
        self,
        ingested_data_path: Optional[str] = None
    ) -> GenerateResult:
        """Run only the generate stage"""
        return self._generate_stage.run(ingested_data_path=ingested_data_path)
    
    def run_transform_only(
        self,
        generated_content: Optional[Dict] = None,
        generated_content_path: Optional[str] = None
    ) -> TransformResult:
        """Run only the transform stage"""
        return self._transform_stage.run(
            generated_content=generated_content,
            generated_content_path=generated_content_path
        )
    
    def run_deploy_only(
        self,
        files: Optional[List[str]] = None,
        dry_run: bool = False
    ) -> DeployResult:
        """Run only the deploy stage"""
        return self._deploy_stage.run(files=files, dry_run=dry_run)
    
    def _build_summary(self, result: PipelineResult) -> Dict[str, Any]:
        """Build execution summary"""
        summary = {
            "duration_seconds": result.duration_seconds,
            "success": result.success
        }
        
        if result.ingest:
            summary["keywords_processed"] = result.ingest.total_keywords
            summary["csv_files_processed"] = len(result.ingest.processed_files)
        
        if result.generate:
            summary["batches_processed"] = result.generate.successful_batches
            summary["total_batches"] = result.generate.total_batches
        
        if result.transform:
            summary["changes_made"] = len(result.transform.changes)
            summary["seo_json_updated"] = result.transform.success
        
        if result.deploy:
            summary["committed"] = result.deploy.committed
            summary["pushed"] = result.deploy.pushed
            if result.deploy.commit_hash:
                summary["commit_hash"] = result.deploy.commit_hash
        
        if result.errors:
            summary["errors"] = result.errors
        
        return summary
    
    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            "config_loaded": bool(self.config._config),
            "git_status": self._deploy_stage.get_status(),
            "input_directory": self.config.input_dir,
            "seo_json_path": self.config.seo_json_path,
            "llm_endpoint": self.config.llm_endpoint
        }
