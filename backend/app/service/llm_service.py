from openai import OpenAI
from app.config import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

def get_llm_client():
    if settings.LLM_PROVIDER == "gemini":
        return OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url=settings.GEMINI_BASE_URL
        )
    else:
        return OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_response(
    query: str,
    context: Optional[str] = None,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None
) -> Dict:
    try:
        client = get_llm_client()
        if model is None:
            model = "gemini-flash-latest" if settings.LLM_PROVIDER == "gemini" else "gpt-3.5-turbo"
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({"role": "system", "content": "You are a helpful assistant."})
        
        if context:
            messages.append({
                "role": "system",
                "content": f"Use the following context to answer the question:\n\n{context}"
            })

        messages.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        logger.info(f"Generated response using {model}")
        
        return {
            "success": True,
            "response": answer,
            "model": model,
            "tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0
        }
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return {
            "success": False,
            "response": f"Error: {str(e)}",
            "model": model,
            "tokens": 0
        }