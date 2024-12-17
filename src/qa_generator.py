"""
Question-answer generation functionality with intelligent chunking and filtering.
"""

import re
from typing import List, Dict, Any
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.evaluation import DatasetGenerator
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from config.settings import GPT_MODEL, TEMPERATURE, OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

class QAGenerator:
    def __init__(self, max_questions_per_chunk: int = 3):
        self.llm = OpenAI(temperature=TEMPERATURE, model=GPT_MODEL)
        self.embed_model = OpenAIEmbedding()
        self.max_questions_per_chunk = max_questions_per_chunk
        Settings.embed_model = self.embed_model
        Settings.llm = self.llm
        
    def split_into_chunks(self, text: str) -> List[str]:
        """Split text into semantic chunks."""
        # Split on major section breaks
        sections = re.split(r'(?=\n(?:Chapter|Part|Epilogue))', text)
        return [s for s in sections if len(s.strip()) > 100]  # Remove very small chunks

    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """Preprocess documents to enhance quality."""
        processed_docs = []
        for doc in documents:
            if hasattr(doc, 'text') and doc.text:
                chunks = self.split_into_chunks(doc.text)
                for chunk in chunks:
                    new_doc = Document(text=chunk)
                    processed_docs.append(new_doc)
        return processed_docs
        
    def generate_qa_pairs(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Generate question-answer pairs from documents."""
        try:
            # Preprocess documents
            processed_docs = self.preprocess_documents(documents)
            logger.info(f"Processing {len(processed_docs)} document chunks")

            # Create vector store index
            vector_index = VectorStoreIndex.from_documents(
                processed_docs,
                embed_model=self.embed_model
            )
            
            # Initialize dataset generator
            data_generator = DatasetGenerator.from_documents(processed_docs)
            
            # Generate questions
            eval_questions = data_generator.generate_questions_from_nodes()
            logger.info(f"Generated {len(eval_questions)} initial questions")
            
            # Limit questions per chunk if needed
            if len(eval_questions) > self.max_questions_per_chunk * len(processed_docs):
                eval_questions = eval_questions[:self.max_questions_per_chunk * len(processed_docs)]
            
            # Generate answers using query engine
            query_engine = vector_index.as_query_engine()
            qa_pairs = []
            
            for i, question in enumerate(eval_questions, 1):
                try:
                    response = query_engine.query(question)
                    qa_pair = {
                        "question": question,
                        "answer": str(response),
                        "sources": [
                            {
                                "text": node.node.get_content(),
                                "score": float(node.score) if hasattr(node, 'score') else None
                            }
                            for node in response.source_nodes
                        ] if hasattr(response, 'source_nodes') else [],
                        "metadata": {
                            "question_number": i,
                            "total_questions": len(eval_questions)
                        }
                    }
                    qa_pairs.append(qa_pair)
                    logger.info(f"Processed question {i}/{len(eval_questions)}")
                except Exception as e:
                    logger.error(f"Error processing question {i}: {str(e)}")
                    continue
            
            return qa_pairs
            
        except Exception as e:
            logger.error(f"Error generating QA pairs: {str(e)}")
            raise