import os

# Ollama settings
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5vl:7b"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_EXCEL = os.path.join(DATA_DIR, "output.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)