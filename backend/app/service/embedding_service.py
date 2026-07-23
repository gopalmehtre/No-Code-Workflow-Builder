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

import httpx

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

def _generate_embeddings_gemini(texts: list) -> list:
    """Generate embeddings using Google's native embedContent API."""
    api_key = settings.gemini_api_key
    model = "gemini-embedding-001"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:batchEmbedContents"
    
    payload = {
        "requests": [
            {
                "model": f"models/{model}",
                "content": {"parts": [{"text": text}]}
            }
            for text in texts
        ]
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, params={"key": api_key}, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Gemini API error: {response.text}")

    data = response.json()
    embeddings = [item.get("values", []) for item in data.get("embeddings", [])]
    return embeddings

def generate_embeddings(texts: list) -> list:
    if not texts:
        return []
        
    try:
        if settings.llm_provider == "gemini":
            embeddings = _generate_embeddings_gemini(texts)
        else:
            client = get_embedding_client()
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=texts
            )
            embeddings = [data.embedding for data in response.data]
            
        if not embeddings or not all(embeddings):
            raise ValueError("Embedding generation failed — got empty embeddings")
            
        return embeddings
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        raise ValueError(f"Failed to generate embeddings: {str(e)}")