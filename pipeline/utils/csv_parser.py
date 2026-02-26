"""
CSV parsing and validation utilities
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


REQUIRED_COLUMNS = [
    "Keyword",
    "Search Volume",
    "Keyword Difficulty",
    "CPC",
    "Position",
    "URL",
    "Trends",
    "Keyword Intents",
    "SERP Features by Keyword",
]

NUMERIC_COLUMNS = ["Search Volume", "Keyword Difficulty", "CPC", "Position"]


def normalize_column_name(name: str) -> str:
    """Normalize column name for matching"""
    return re.sub(r"\s+", " ", str(name).strip().lower())


def find_csv_files(directory: str) -> List[str]:
    """Find all CSV files in a directory"""
    csv_files = []
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return csv_files
    
    for file_path in dir_path.glob("*.csv"):
        if not file_path.name.startswith('.'):
            csv_files.append(str(file_path))
    
    return sorted(csv_files)


def validate_csv_columns(df: pd.DataFrame, required: List[str]) -> Tuple[bool, List[str], Dict[str, str]]:
    """
    Validate that DataFrame has required columns.
    Returns: (is_valid, missing_columns, column_mapping)
    """
    norm_to_required = {normalize_column_name(c): c for c in required}
    column_mapping = {}
    missing = []
    
    for col in df.columns:
        norm_col = normalize_column_name(col)
        if norm_col in norm_to_required:
            column_mapping[col] = norm_to_required[norm_col]
    
    for req_col in required:
        if req_col not in column_mapping.values():
            missing.append(req_col)
    
    is_valid = len(missing) == 0
    return is_valid, missing, column_mapping


def clean_csv(
    csv_path: str,
    required_columns: Optional[List[str]] = None,
    max_rows: Optional[int] = None
) -> pd.DataFrame:
    """
    Load and clean CSV file.
    
    Args:
        csv_path: Path to CSV file
        required_columns: List of required column names
        max_rows: Maximum number of rows to return
        
    Returns:
        Cleaned DataFrame with standardized columns
    """
    if required_columns is None:
        required_columns = REQUIRED_COLUMNS
    
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    
    is_valid, missing, column_mapping = validate_csv_columns(df, required_columns)
    
    if column_mapping:
        df = df.rename(columns=column_mapping)
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    
    df = df[required_columns]
    
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x if x is None else (x.strip() if isinstance(x, str) else x)
        )
    
    for num_col in NUMERIC_COLUMNS:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
    
    df = df.dropna(how="all", subset=required_columns)
    
    if "Keyword" in df.columns:
        df = df.drop_duplicates(subset=["Keyword"])
    
    if max_rows is not None and len(df) > max_rows:
        df = df.head(max_rows)
    
    return df


def calculate_opportunity_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate opportunity score for keywords.
    Higher volume + lower difficulty = higher opportunity
    """
    df = df.copy()
    
    if "Search Volume" in df.columns and "Keyword Difficulty" in df.columns:
        max_volume = df["Search Volume"].max() or 1
        max_difficulty = df["Keyword Difficulty"].max() or 1
        
        volume_score = df["Search Volume"].fillna(0) / max_volume
        difficulty_score = 1 - (df["Keyword Difficulty"].fillna(0) / max_difficulty)
        
        df["opportunity_score"] = (volume_score * 0.6 + difficulty_score * 0.4) * 100
        df["opportunity_score"] = df["opportunity_score"].round(2)
    
    return df


def get_top_keywords(
    df: pd.DataFrame,
    n: int = 100,
    sort_by: str = "opportunity_score"
) -> pd.DataFrame:
    """
    Get top N keywords by specified metric.
    """
    if sort_by == "opportunity_score" and sort_by not in df.columns:
        df = calculate_opportunity_score(df)
        sort_by = "opportunity_score"
    elif sort_by not in df.columns:
        sort_by = "Search Volume"
    
    df_sorted = df.sort_values(by=sort_by, ascending=False)
    return df_sorted.head(n)


def archive_csv(csv_path: str, archive_dir: str) -> str:
    """
    Move processed CSV to archive directory.
    Returns the archived file path.
    """
    from datetime import datetime
    import shutil
    
    archive_path = Path(archive_dir)
    archive_path.mkdir(parents=True, exist_ok=True)
    
    original_name = Path(csv_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = Path(csv_path).suffix
    
    archived_name = f"{original_name}_processed_{timestamp}{ext}"
    archived_path = archive_path / archived_name
    
    shutil.move(csv_path, archived_path)
    
    return str(archived_path)
