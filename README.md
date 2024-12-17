# QA Generator

A Python-based tool for generating high-quality Dataset genarator pairs from documents. The system uses LlamaIndex and OpenAI to create contextually relevant QA pairs while maintaining semantic meaning and avoiding duplicates.

## Features

- **Intelligent Text Processing**
  - Semantic chunking based on document structure
  - Context-aware question generation
  - De-duplication of similar questions
  - Source tracking for answers

- **Multiple Export Formats**
  - JSON output with full metadata and source information
  - CSV output for easy viewing and analysis
  - Configurable output formatting

- **Configurable Settings**
  - Adjustable number of questions per chunk
  - Customizable similarity thresholds for deduplication
  - Fine-tunable question generation parameters

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/qa_generator.git
cd qa_generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
Create a `.env` file in the project root and add:
```
OPENAI_API_KEY=your-api-key-here
```

## Project Structure

```
qa_generator/
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration settings
├── data/
│   ├── input/               # Place input documents here
│   └── output/              # Generated QA pairs will be saved here
├── src/
│   ├── __init__.py
│   ├── document_loader.py   # Document loading and preprocessing
│   ├── qa_generator.py      # Question-answer generation logic
│   └── exporters/
│       ├── __init__.py
│       ├── json_exporter.py
│       └── csv_exporter.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── README.md
└── main.py
```

## Usage

1. Place your document(s) in the `data/input` directory

2. Run the generator:
```bash
python main.py
```

3. Find the generated QA pairs in `data/output` directory:
   - `qa_pairs_[timestamp].json` - Full QA pairs with metadata
   - `qa_pairs_[timestamp].csv` - Simplified format for spreadsheet viewing

## Configuration

Key settings can be adjusted in `config/settings.py`:

```python
# Maximum questions per document chunk
MAX_QUESTIONS_PER_CHUNK = 3

# Similarity threshold for deduplication (0.0 to 1.0)
SIMILARITY_THRESHOLD = 0.7

# OpenAI model settings
GPT_MODEL = "gpt-4"
TEMPERATURE = 0
```

## Generated Output Format

### JSON Output
```json
{
  "question": "Example question?",
  "answer": "Detailed answer",
  "sources": [
    {
      "text": "Source text",
      "score": 0.8
    }
  ],
  "metadata": {
    "question_number": 1,
    "total_questions": 50
  }
}
```

### CSV Output
- question
- answer
- sources (combined)
- source_scores
- question_number
- total_questions

## Customization

### Adding New Document Types

Extend the `DocumentLoader` class in `src/document_loader.py` to support additional document types:

```python
def load_new_format(self, file_path: str) -> Document:
    # Implement loading logic here
    pass
```

### Custom Question Generation

Modify the question generation logic in `src/qa_generator.py`:

```python
def generate_chunk_questions(self, chunk: str) -> List[str]:
    # Implement custom question generation logic
    pass
```



## Acknowledgments

- LlamaIndex for document processing
- OpenAI for language model support
- All contributors and maintainers