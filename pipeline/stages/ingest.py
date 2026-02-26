"""
Stage 1: Ingest - CSV Input Processing and Validation
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from ..utils.config import get_config
from ..utils.csv_parser import (
    archive_csv,
    calculate_opportunity_score,
    clean_csv,
    find_csv_files,
    get_top_keywords,
)
from ..utils.logger import get_logger


@dataclass
class IngestResult:
    """Result of the ingest stage"""
    success: bool
    csv_files_found: int = 0
    total_keywords: int = 0
    processed_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    data_path: Optional[str] = None


class IngestStage:
    """Stage 1: Ingest CSV files and validate keyword data"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self._data = None
    
    def run(
        self,
        input_path: Optional[str] = None,
        max_keywords: Optional[int] = None,
        archive_after: bool = True
    ) -> IngestResult:
        """
        Run the ingest stage.
        
        Args:
            input_path: Optional specific CSV file path
            max_keywords: Maximum number of keywords to process
            archive_after: Archive CSV files after processing
            
        Returns:
            IngestResult with processed data info
        """
        self.logger.stage("INGEST", "Starting CSV ingestion...")
        
        result = IngestResult(success=False)
        
        input_dir = self.config.input_dir
        if input_path:
            if os.path.exists(input_path):
                csv_files = [input_path]
            else:
                result.errors.append(f"Input file not found: {input_path}")
                return result
        else:
            csv_files = find_csv_files(input_dir)
        
        result.csv_files_found = len(csv_files)
        
        if not csv_files:
            self.logger.warning("No CSV files found in input directory")
            result.errors.append("No CSV files found")
            return result
        
        self.logger.info(f"Found {len(csv_files)} CSV file(s)")
        
        all_data = []
        required_columns = self.config.required_columns
        max_kw = max_keywords or self.config.get('input', 'max_keywords', default=100)
        
        for csv_file in csv_files:
            self.logger.info(f"Processing: {csv_file}")
            
            try:
                df = clean_csv(csv_file, required_columns=required_columns)
                df = calculate_opportunity_score(df)
                df = get_top_keywords(df, n=max_kw, sort_by="opportunity_score")
                
                self.logger.info(f"  - Extracted {len(df)} keywords")
                
                all_data.append(df)
                result.processed_files.append(csv_file)
                
            except Exception as e:
                error_msg = f"Error processing {csv_file}: {str(e)}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
        
        if not all_data:
            result.errors.append("No valid data extracted from CSV files")
            return result
        
        import pandas as pd
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=["Keyword"])
        combined_df = get_top_keywords(combined_df, n=max_kw, sort_by="opportunity_score")
        
        self._data = combined_df
        result.total_keywords = len(combined_df)
        result.success = True
        
        cache_dir = self.config.cache_dir
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        cache_file = os.path.join(cache_dir, "ingested_data.csv")
        combined_df.to_csv(cache_file, index=False)
        result.data_path = cache_file
        
        self.logger.success(f"Ingested {result.total_keywords} keywords from {len(result.processed_files)} file(s)")
        
        if archive_after:
            processed_dir = self.config.processed_dir
            Path(processed_dir).mkdir(parents=True, exist_ok=True)
            
            for csv_file in result.processed_files:
                try:
                    archived = archive_csv(csv_file, processed_dir)
                    self.logger.info(f"Archived: {archived}")
                except Exception as e:
                    self.logger.warning(f"Could not archive {csv_file}: {e}")
        
        return result
    
    @property
    def data(self):
        """Get the ingested DataFrame"""
        return self._data
