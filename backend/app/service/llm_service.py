from openai import OpenAI
import logging
from app.config import settings

logger = logging.getLogger(__name__)

def get_llm_client():
    if settings.llm_provider == "gemini":
        return OpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url
        )
    else:
        return OpenAI(api_key=settings.openai_api_key)

def generate_response(query: str, context: str = "", system_prompt: str = None, model: str = None) -> dict:
    try:
        client = get_llm_client()
        
        if not model:
            model = "gemini-flash-latest" if settings.llm_provider == "gemini" else "gpt-3.5-turbo"
        
        if not system_prompt:
            system_prompt = "You are a helpful PDF assistant. Answer questions based on the provided context. If the context doesn't contain relevant information, say so."
        
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"})
        else:
            messages.append({"role": "user", "content": query})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return {
            "response": response.choices[0].message.content,
            "model": model
        }
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return {
            "response": f"Error generating response: {str(e)}",
            "error": str(e)
        }