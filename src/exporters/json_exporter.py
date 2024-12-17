# json_exporter.py
"""
JSON export functionality for QA pairs.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from config.settings import JSON_INDENT

class JsonExporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def export(self, qa_pairs: List[Dict[str, Any]], filename: str) -> Path:
        """
        Export QA pairs to JSON file.
        
        Args:
            qa_pairs (List[Dict[str, Any]]): QA pairs to export
            filename (str): Output filename
            
        Returns:
            Path: Path to the exported file
        """
        output_path = self.output_dir / f"{filename}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, indent=JSON_INDENT, ensure_ascii=False)
        return output_path