from openai import OpenAI
import logging
from app.config import settings

logger = logging.getLogger(__name__)

def get_embedding_client():
    if settings.llm_provider == "gemini":
        return OpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url
        )
    else:
        return OpenAI(api_key=settings.openai_api_key)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """Split text into overlapping chunks for better retrieval."""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        if end < text_length:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            if break_point > chunk_size // 2:
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return [c for c in chunks if c]

def generate_embeddings(texts: list) -> list:
    try:
        client = get_embedding_client()
        model = "text-embedding-004" if settings.llm_provider == "gemini" else "text-embedding-ada-002"
        
        embeddings = []
        for text in texts:
            response = client.embeddings.create(
                model=model,
                input=text
            )
            embeddings.append(response.data[0].embedding)
        
        return embeddings
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        return []