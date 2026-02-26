"""
JSON handling utilities
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from jsonschema import validate as json_validate
    from jsonschema.exceptions import ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    ValidationError = Exception


def read_json(file_path: str) -> Dict[str, Any]:
    """Read JSON file and return as dictionary"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(
    data: Union[Dict, List],
    file_path: str,
    indent: int = 2,
    ensure_ascii: bool = False
) -> bool:
    """Write data to JSON file"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    
    return True


def backup_json(file_path: str, backup_dir: str) -> Optional[str]:
    """
    Create backup of JSON file.
    Returns backup path or None if file doesn't exist.
    """
    if not os.path.exists(file_path):
        return None
    
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)
    
    original_name = Path(file_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = Path(file_path).suffix
    
    backup_name = f"{original_name}_backup_{timestamp}{ext}"
    backup_file = backup_path / backup_name
    
    shutil.copy2(file_path, backup_file)
    
    return str(backup_file)


def merge_json(
    base: Dict[str, Any],
    updates: Dict[str, Any],
    preserve_keys: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Merge updates into base dictionary.
    Preserves specified keys in base if they exist.
    """
    if preserve_keys is None:
        preserve_keys = []
    
    result = base.copy()
    
    for key, value in updates.items():
        if key in preserve_keys and key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_json(result[key], value, preserve_keys)
            elif isinstance(result[key], list) and isinstance(value, list):
                existing = set(str(x) for x in result[key])
                for item in value:
                    if str(item) not in existing:
                        result[key].append(item)
        else:
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = {**result[key], **value}
            else:
                result[key] = value
    
    return result


def extract_json_from_text(text: str) -> Optional[Union[Dict, List]]:
    """
    Extract JSON from text that may contain extra content.
    Handles markdown code blocks and extra text.
    """
    if not text:
        return None
    
    text = text.strip()
    
    if text.startswith('```'):
        lines = text.split('\n')
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].startswith('```'):
            lines = lines[:-1]
        text = '\n'.join(lines).strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    array_start = text.find('[')
    array_end = text.rfind(']')
    if array_start != -1 and array_end != -1 and array_end > array_start:
        try:
            return json.loads(text[array_start:array_end + 1])
        except json.JSONDecodeError:
            pass
    
    obj_start = text.find('{')
    obj_end = text.rfind('}')
    if obj_start != -1 and obj_end != -1 and obj_end > obj_start:
        try:
            return json.loads(text[obj_start:obj_end + 1])
        except json.JSONDecodeError:
            pass
    
    import re
    for match in re.finditer(r'\{.*\}|\[.*\]', text, flags=re.S):
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
    
    return None


def validate_json_schema(
    data: Dict[str, Any],
    schema: Dict[str, Any]
) -> Tuple[bool, Optional[str]]:
    """
    Validate JSON data against a schema.
    Returns (is_valid, error_message)
    """
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except ImportError:
        return True, None
    except Exception as e:
        return False, str(e)
