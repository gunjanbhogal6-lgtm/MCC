"""
Stage 3: Transform - Merge generated content into seo.json
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.config import get_config
from ..utils.json_handler import backup_json, merge_json, read_json, write_json
from ..utils.logger import get_logger


PRESERVE_KEYS = [
    "site",
    "sections",
    "footer"
]


@dataclass
class TransformResult:
    """Result of the transform stage"""
    success: bool
    seo_json_path: Optional[str] = None
    backup_path: Optional[str] = None
    changes: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class TransformStage:
    """Stage 3: Transform generated content into seo.json format"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self._output_data = None
    
    def run(
        self,
        generated_content: Optional[Dict[str, Any]] = None,
        generated_content_path: Optional[str] = None,
        seo_json_path: Optional[str] = None,
        create_backup: bool = True
    ) -> TransformResult:
        """
        Run the transform stage.
        
        Args:
            generated_content: Direct dict of generated content
            generated_content_path: Path to generated content JSON
            seo_json_path: Path to target seo.json file
            create_backup: Whether to backup existing seo.json
            
        Returns:
            TransformResult with update information
        """
        self.logger.stage("TRANSFORM", "Transforming generated content into seo.json...")
        
        result = TransformResult(success=False)
        
        content = generated_content
        if content is None:
            cache_file = generated_content_path or os.path.join(
                self.config.cache_dir, "generated_content.json"
            )
            if not os.path.exists(cache_file):
                result.errors.append("No generated content found. Run generate stage first.")
                return result
            with open(cache_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
        
        if not content:
            result.errors.append("Generated content is empty")
            return result
        
        target_path = seo_json_path or self.config.seo_json_path
        
        if not os.path.exists(target_path):
            result.errors.append(f"Target seo.json not found: {target_path}")
            return result
        
        if create_backup:
            backup_dir = self.config.get('output', 'backup_directory', default='data/backups')
            backup_path = backup_json(target_path, backup_dir)
            if backup_path:
                result.backup_path = backup_path
                self.logger.info(f"Backup created: {backup_path}")
        
        existing_data = read_json(target_path)
        
        updated_data = self._merge_seo_content(existing_data, content)
        
        changes = self._detect_changes(existing_data, updated_data)
        result.changes = changes
        
        write_json(updated_data, target_path)
        result.seo_json_path = target_path
        result.success = True
        self._output_data = updated_data
        
        self.logger.success(f"Updated seo.json with {len(changes)} changes")
        
        return result
    
    def _merge_seo_content(
        self,
        existing: Dict[str, Any],
        generated: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge generated SEO content into existing seo.json structure"""
        result = existing.copy()
        
        if "seo" not in result:
            result["seo"] = {}
        
        seo_section = result["seo"]
        
        if generated.get("metaTitle"):
            old_title = seo_section.get("metaTitle", "")
            seo_section["metaTitle"] = generated["metaTitle"]
        
        if generated.get("metaDescription"):
            seo_section["metaDescription"] = generated["metaDescription"]
        
        if generated.get("focusKeyword"):
            seo_section["focusKeyword"] = generated["focusKeyword"]
        
        if generated.get("lsiKeywords"):
            existing_lsi = set(seo_section.get("lsiKeywords", []))
            new_lsi = set(generated["lsiKeywords"])
            seo_section["lsiKeywords"] = list(existing_lsi | new_lsi)
        
        if generated.get("targetAudience"):
            seo_section["targetAudience"] = generated["targetAudience"]
        
        if generated.get("pageGoal"):
            seo_section["pageGoal"] = generated["pageGoal"]
        
        if generated.get("competitorSentence"):
            seo_section["competitorSentence"] = generated["competitorSentence"]
        
        if "keywords" not in result:
            result["keywords"] = {"primary": [], "secondary": []}
        
        if generated.get("primaryKeywords"):
            existing_primary = set(result["keywords"].get("primary", []))
            new_primary = set(generated["primaryKeywords"])
            result["keywords"]["primary"] = list(existing_primary | new_primary)
        
        if generated.get("lsiKeywords"):
            existing_secondary = set(result["keywords"].get("secondary", []))
            new_secondary = set(generated["lsiKeywords"])
            result["keywords"]["secondary"] = list(existing_secondary | new_secondary)
        
        result["_lastUpdated"] = datetime.now().isoformat()
        
        return result
    
    def _detect_changes(
        self,
        old: Dict[str, Any],
        new: Dict[str, Any]
    ) -> List[str]:
        """Detect what changed between old and new seo.json"""
        changes = []
        
        old_seo = old.get("seo", {})
        new_seo = new.get("seo", {})
        
        if old_seo.get("metaTitle") != new_seo.get("metaTitle"):
            changes.append("metaTitle updated")
        
        if old_seo.get("metaDescription") != new_seo.get("metaDescription"):
            changes.append("metaDescription updated")
        
        if old_seo.get("focusKeyword") != new_seo.get("focusKeyword"):
            changes.append("focusKeyword updated")
        
        old_lsi = set(old_seo.get("lsiKeywords", []))
        new_lsi = set(new_seo.get("lsiKeywords", []))
        added_lsi = new_lsi - old_lsi
        if added_lsi:
            changes.append(f"Added {len(added_lsi)} LSI keywords")
        
        old_primary = set(old.get("keywords", {}).get("primary", []))
        new_primary = set(new.get("keywords", {}).get("primary", []))
        added_primary = new_primary - old_primary
        if added_primary:
            changes.append(f"Added {len(added_primary)} primary keywords")
        
        return changes
    
    @property
    def output_data(self) -> Optional[Dict[str, Any]]:
        """Get the transformed output data"""
        return self._output_data
