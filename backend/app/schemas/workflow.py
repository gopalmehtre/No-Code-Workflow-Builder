from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Node]
    edges: List[Edge]
    config: Optional[Dict[str, Any]] = None

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[List[Node]] = None
    edges: Optional[List[Edge]] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    nodes: List[Dict]
    edges: List[Dict]
    config: Optional[Dict]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class WorkflowValidateRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class WorkflowValidateResponse(BaseModel):
    valid: bool
    message: str

class WorkflowExecuteRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    query: str
    workflow_id: Optional[int] = None

class WorkflowExecuteResponse(BaseModel):
    success: bool
    query: str
    response: str
    execution_log: List[Dict]
    metadata: Optional[Dict] = None
    error: Optional[str] = None