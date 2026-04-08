import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

QDRANT_PATH = "qdrant_db"
COLLECTION_NAME = "enterprise_data"

BM25_PATH = "bm25_corpus.pkl"
STRUCTURED_PATH = "structured.pkl"

GROQ_MODEL = "openai/gpt-oss-20b"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")