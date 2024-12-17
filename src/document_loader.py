"""
Document loading and preprocessing functionality.
"""

from pathlib import Path
from typing import List
from llama_index.core import SimpleDirectoryReader, Document

class DocumentLoader:
    def __init__(self, input_dir: Path):
        self.input_dir = input_dir

    def load_documents(self) -> List[Document]:
        """
        Load documents from the input directory.
        
        Returns:
            List[Document]: List of loaded documents
        """
        try:
            reader = SimpleDirectoryReader(input_dir=str(self.input_dir))
            documents = reader.load_data()
            return documents
        except Exception as e:
            raise Exception(f"Error loading documents: {str(e)}")

    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """
        Preprocess the loaded documents.
        
        Args:
            documents (List[Document]): List of documents to preprocess
            
        Returns:
            List[Document]: Preprocessed documents
        """
        # Add any preprocessing steps here (e.g., cleaning, filtering)
        return documents