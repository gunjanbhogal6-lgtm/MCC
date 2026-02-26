"""
Stage 2: Generate - LLM-powered SEO Content Generation
"""

import json
import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..prompts.seo_prompts import SEO_MASTER_PROMPT, get_seo_prompts, validate_seo_content
from ..utils.config import get_config
from ..utils.json_handler import extract_json_from_text
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger


@dataclass
class GenerateResult:
    """Result of the generate stage"""
    success: bool
    total_batches: int = 0
    successful_batches: int = 0
    generated_content: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    output_path: Optional[str] = None


class GenerateStage:
    """Stage 2: Generate SEO content using LLM"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self.llm_client = LLMClient(
            endpoint=self.config.llm_endpoint,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            batch_size=self.config.batch_size
        )
        self._generated_content = None
    
    def run(
        self,
        ingested_data_path: Optional[str] = None,
        batch_size: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> GenerateResult:
        """
        Run the generate stage.
        
        Args:
            ingested_data_path: Path to ingested CSV data
            batch_size: Number of rows per LLM request
            system_prompt: Custom system prompt for LLM
            
        Returns:
            GenerateResult with generated SEO content
        """
        self.logger.stage("GENERATE", "Starting SEO content generation...")
        
        result = GenerateResult(success=False)
        
        import pandas as pd
        
        if ingested_data_path and os.path.exists(ingested_data_path):
            df = pd.read_csv(ingested_data_path)
        else:
            cache_file = os.path.join(self.config.cache_dir, "ingested_data.csv")
            if not os.path.exists(cache_file):
                result.errors.append("No ingested data found. Run ingest stage first.")
                return result
            df = pd.read_csv(cache_file)
        
        total_rows = len(df)
        batch_sz = batch_size or self.config.batch_size
        num_batches = math.ceil(total_rows / batch_sz)
        
        self.logger.info(f"Processing {total_rows} keywords in {num_batches} batch(es)")
        
        result.total_batches = num_batches
        all_generated = []
        
        sys_prompt = system_prompt or SEO_MASTER_PROMPT
        
        for i in range(num_batches):
            start_idx = i * batch_sz
            end_idx = min(start_idx + batch_sz, total_rows)
            batch_df = df.iloc[start_idx:end_idx]
            
            self.logger.info(f"Processing batch {i+1}/{num_batches} (rows {start_idx}-{end_idx})...")
            
            csv_text = batch_df.to_csv(index=False)
            
            llm_result = self.llm_client.generate(csv_text, sys_prompt)
            
            if llm_result["success"] and llm_result["response"]:
                try:
                    parsed = extract_json_from_text(llm_result["response"])
                    
                    if parsed:
                        if isinstance(parsed, list):
                            all_generated.extend(parsed)
                        else:
                            all_generated.append(parsed)
                        result.successful_batches += 1
                        self.logger.success(f"Batch {i+1} generated successfully")
                    else:
                        result.errors.append(f"Batch {i+1}: Could not parse JSON response")
                        
                except Exception as e:
                    result.errors.append(f"Batch {i+1}: Parse error - {str(e)}")
            else:
                error = llm_result.get("error", "Unknown error")
                result.errors.append(f"Batch {i+1}: LLM error - {error}")
        
        if all_generated:
            merged_content = self._merge_generated_content(all_generated)
            validated_content = validate_seo_content(merged_content)
            result.generated_content = validated_content
            self._generated_content = validated_content
            result.success = True
            
            cache_dir = self.config.cache_dir
            cache_file = os.path.join(cache_dir, "generated_content.json")
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(validated_content, f, indent=2)
            result.output_path = cache_file
            
            self.logger.success(f"Generated SEO content from {result.successful_batches}/{num_batches} batches")
            self.logger.info(f"Meta Title: {validated_content.get('metaTitle', '')[:60]} chars")
            self.logger.info(f"Meta Description: {len(validated_content.get('metaDescription', ''))} chars")
        else:
            result.errors.append("No content was successfully generated")
        
        return result
    
    def _merge_generated_content(self, content_list: List[Dict]) -> Dict[str, Any]:
        """Merge multiple generated content pieces into one"""
        merged = {
            "metaTitle": "",
            "metaDescription": "",
            "focusKeyword": "",
            "lsiKeywords": [],
            "primaryKeywords": [],
            "targetAudience": "",
            "pageGoal": "MoFu",
            "competitorSentence": ""
        }
        
        all_lsi = set()
        all_primary = set()
        
        best_title = ""
        best_title_score = 0
        best_desc = ""
        best_desc_score = 0
        
        for content in content_list:
            title = content.get("metaTitle", "")
            if 50 <= len(title) <= 60 and len(title) > best_title_score:
                best_title = title
                best_title_score = len(title)
            elif not merged["metaTitle"] and title:
                merged["metaTitle"] = title
            
            desc = content.get("metaDescription", "")
            if 150 <= len(desc) <= 160 and len(desc) > best_desc_score:
                best_desc = desc
                best_desc_score = len(desc)
            elif not merged["metaDescription"] and desc:
                merged["metaDescription"] = desc
            
            if not merged["focusKeyword"] and content.get("focusKeyword"):
                merged["focusKeyword"] = content["focusKeyword"]
            if not merged["targetAudience"] and content.get("targetAudience"):
                merged["targetAudience"] = content["targetAudience"]
            if not merged["competitorSentence"] and content.get("competitorSentence"):
                merged["competitorSentence"] = content["competitorSentence"]
            
            if content.get("lsiKeywords"):
                all_lsi.update(content["lsiKeywords"])
            if content.get("primaryKeywords"):
                all_primary.update(content["primaryKeywords"])
        
        if best_title:
            merged["metaTitle"] = best_title
        if best_desc:
            merged["metaDescription"] = best_desc
        
        merged["lsiKeywords"] = list(all_lsi)[:25]
        merged["primaryKeywords"] = list(all_primary)[:15]
        
        return merged
    
    @property
    def generated_content(self) -> Optional[Dict[str, Any]]:
        """Get the generated SEO content"""
        return self._generated_content
