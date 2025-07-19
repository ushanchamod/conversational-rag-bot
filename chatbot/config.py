import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-3.5-turbo"
CHROMA_PERSIST_DIR = "chroma_db"
PDF_PATH = "bse-degree-info.pdf"
TEXT_PATH = "bse-degree-info.txt"


