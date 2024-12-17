"""
CSV export functionality for QA pairs.
"""

import csv
from pathlib import Path
from typing import List, Dict, Any
from config.settings import CSV_ENCODING

class CsvExporter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        
    def flatten_qa_pair(self, qa_pair: Dict[str, Any]) -> Dict[str, str]:
        """Flatten nested dictionary structure for CSV export."""
        flattened = {
            'question': qa_pair['question'],
            'answer': qa_pair['answer'],
            'sources': '; '.join(str(source['text']) for source in qa_pair.get('sources', [])),
            'source_scores': '; '.join(str(source.get('score', '')) for source in qa_pair.get('sources', [])),
            'question_number': str(qa_pair.get('metadata', {}).get('question_number', '')),
            'total_questions': str(qa_pair.get('metadata', {}).get('total_questions', ''))
        }
        return flattened

    def export(self, qa_pairs: List[Dict[str, Any]], filename: str) -> Path:
        """
        Export QA pairs to CSV file.
        
        Args:
            qa_pairs (List[Dict[str, Any]]): QA pairs to export
            filename (str): Output filename
            
        Returns:
            Path: Path to the exported file
        """
        output_path = self.output_dir / f"{filename}.csv"
        
        # Convert complex dictionaries to flat structure
        flattened_pairs = [self.flatten_qa_pair(qa) for qa in qa_pairs]
        
        if not flattened_pairs:
            raise ValueError("No QA pairs to export")
            
        # Get fieldnames from first item
        fieldnames = list(flattened_pairs[0].keys())
        
        with open(output_path, 'w', encoding=CSV_ENCODING, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_pairs)
                
        return output_path