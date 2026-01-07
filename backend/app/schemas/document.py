from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    filename: str
    collection_name: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    file_size: Optional[int]
    content_preview: Optional[str]
    status: str
    collection_name: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    document: Optional[DocumentResponse] = None
    error: Optional[str] = None