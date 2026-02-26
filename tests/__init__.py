"""
Tests for AutoSEO Pipeline
"""

from pipeline.utils import csv_parser, json_handler


class TestCSVParser:
    """Tests for CSV parser utilities"""
    
    def test_normalize_column_name(self):
        assert csv_parser.normalize_column_name("Keyword") == "keyword"
        assert csv_parser.normalize_column_name("  Search Volume  ") == "search volume"
        assert csv_parser.normalize_column_name("Keyword\nIntents") == "keyword intents"
    
    def test_find_csv_files_empty(self, tmp_path):
        files = csv_parser.find_csv_files(str(tmp_path))
        assert files == []
    
    def test_find_csv_files(self, tmp_path):
        (tmp_path / "test.csv").write_text("Keyword,Volume\ntest,100")
        (tmp_path / "other.csv").write_text("Keyword,Volume\nother,200")
        
        files = csv_parser.find_csv_files(str(tmp_path))
        assert len(files) == 2


class TestJSONHandler:
    """Tests for JSON handler utilities"""
    
    def test_extract_json_from_text_valid(self):
        text = '{"key": "value"}'
        result = json_handler.extract_json_from_text(text)
        assert result == {"key": "value"}
    
    def test_extract_json_from_text_with_extra(self):
        text = 'Here is some JSON: {"key": "value"} and more text'
        result = json_handler.extract_json_from_text(text)
        assert result == {"key": "value"}
    
    def test_extract_json_from_text_markdown(self):
        text = '```json\n{"key": "value"}\n```'
        result = json_handler.extract_json_from_text(text)
        assert result == {"key": "value"}
    
    def test_extract_json_from_text_array(self):
        text = '[{"id": 1}, {"id": 2}]'
        result = json_handler.extract_json_from_text(text)
        assert result == [{"id": 1}, {"id": 2}]
    
    def test_extract_json_from_text_invalid(self):
        text = "not json at all"
        result = json_handler.extract_json_from_text(text)
        assert result is None
    
    def test_merge_json(self):
        base = {"key1": "value1", "list": ["a"]}
        updates = {"key2": "value2", "list": ["b"]}
        result = json_handler.merge_json(base, updates)
        assert result["key1"] == "value1"
        assert result["key2"] == "value2"
