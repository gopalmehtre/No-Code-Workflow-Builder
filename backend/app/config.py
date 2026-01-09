import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='ignore'
    )
    
    # Database
    database_url: str = "postgresql://postgres:postgres@postgres:5432/workflow_db"
    
    # ChromaDB
    chroma_host: str = "chromadb"
    chroma_port: int = 8000
    chroma_persist_directory: str = "./chroma_data"
    
    # Gemini API
    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # OpenAI (optional fallback)
    openai_api_key: str = ""
    
    # LLM Provider
    llm_provider: str = "gemini"
    
    # CORS
    allowed_origins: str = '["http://localhost:3000","http://localhost:5173","http://localhost:80","http://localhost"]'
    
    # Application
    app_name: str = "FlowAI Studio"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8080
    
    # File Upload
    upload_dir: str = "./uploads"
    max_upload_size: int = 10485760

settings = Settings()