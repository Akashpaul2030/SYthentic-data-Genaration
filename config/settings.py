"""
Configuration settings for the QA Generator.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

# Create directories if they don't exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Make sure OpenAI key is set for the openai package
import openai
openai.api_key = OPENAI_API_KEY

GPT_MODEL = "gpt-4"
TEMPERATURE = 0

# LlamaIndex settings
EMBED_MODEL = "text-embedding-ada-002"

# Export settings
JSON_INDENT = 2
CSV_ENCODING = "utf-8"