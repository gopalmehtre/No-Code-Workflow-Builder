from openai import OpenAI
from app.config import settings
from typing import List, Union
import logging

logger = logging.getLogger(__name__)

def get_embedding_client():
    if settings.LLM_PROVIDER == "gemini":
        return OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url=settings.GEMINI_BASE_URL
        )
    else:
        return OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_embeddings(texts: Union[str, List[str]], model: str= None) -> List[List[float]]:

    try:
        client= get_embedding_client()

        if isinstance(texts, str):
            texts = [texts]

        if model is None:
            model = "text-embedding-004" if settings.LLM_PROVIDER == "gemini" else "text-embedding-ada-002"

        response = client.embeddings.create(
            input=texts,
            model=model
        )

        embeddings = [item.embedding for item in response.data]

        logger.info(f"Generated {len(embeddings)} embeddings using {model}")
        return embeddings

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)} ")
        raise

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks