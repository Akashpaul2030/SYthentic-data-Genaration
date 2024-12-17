"""
Main entry point for the QA Generator.
"""

import logging
from datetime import datetime
from config.settings import INPUT_DIR, OUTPUT_DIR
from src.document_loader import DocumentLoader
from src.qa_generator import QAGenerator
from src.exporters.json_exporter import JsonExporter
from src.exporters.csv_exporter import CsvExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        doc_loader = DocumentLoader(INPUT_DIR)
        qa_generator = QAGenerator(max_questions_per_chunk=3)  # Limit questions per chunk
        json_exporter = JsonExporter(OUTPUT_DIR)
        csv_exporter = CsvExporter(OUTPUT_DIR)

        # Load and preprocess documents
        logger.info("Loading documents...")
        documents = doc_loader.load_documents()
        documents = doc_loader.preprocess_documents(documents)
        logger.info(f"Loaded {len(documents)} documents")

        # Generate QA pairs
        logger.info("Generating QA pairs...")
        qa_pairs = qa_generator.generate_qa_pairs(documents)
        logger.info(f"Generated {len(qa_pairs)} QA pairs")

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"qa_pairs_{timestamp}"

        # Export results
        logger.info("Exporting results...")
        json_path = json_exporter.export(qa_pairs, base_filename)
        csv_path = csv_exporter.export(qa_pairs, base_filename)
        
        logger.info(f"Results exported to:")
        logger.info(f"- JSON: {json_path}")
        logger.info(f"- CSV: {csv_path}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()