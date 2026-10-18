import os

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Retrieval
TOP_K = int(os.getenv("TOP_K", "3"))

# Vector database
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "school_courses_v2"

# Prefixes expected by nomic-embed-text (see evaluation/results)
EMBEDDING_QUERY_PREFIX = "search_query: "
EMBEDDING_DOC_PREFIX = "search_document: "


# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
