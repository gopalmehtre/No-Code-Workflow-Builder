from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    workflow_id: int
    query: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    query: str
    response: str
    workflow_id: int
    execution_time: Optional[int] = None
    error: Optional[str] = None

class ChatHistoryResponse(BaseModel):
    id: int
    workflow_id: Optional[int]
    session_id: Optional[str]
    query: str
    response: str
    context_used: Optional[str]
    execution_time: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True