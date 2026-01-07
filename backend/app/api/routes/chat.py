from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time

from app.database import get_db
from app.models.workflow import Workflow
from app.models.chat import ChatHistory
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.service.workflow_executor import execute_workflow

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
def chat_with_workflow(request: ChatRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    workflow = db.query(Workflow).filter(Workflow.id == request.workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    try:
        result = execute_workflow(
            nodes=workflow.nodes,
            edges=workflow.edges,
            query=request.query
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        if result.get("success"):
            response_text = result.get("response", "")
            
            chat_history = ChatHistory(
                workflow_id=request.workflow_id,
                session_id=request.session_id,
                query=request.query,
                response=response_text,
                context_used=result.get("metadata", {}).get("context", ""),
                execution_time=execution_time
            )
            db.add(chat_history)
            db.commit()
            
            return ChatResponse(
                success=True,
                query=request.query,
                response=response_text,
                workflow_id=request.workflow_id,
                execution_time=execution_time
            )
        else:
            return ChatResponse(
                success=False,
                query=request.query,
                response="",
                workflow_id=request.workflow_id,
                execution_time=execution_time,
                error=result.get("error", "Unknown error")
            )
    
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        return ChatResponse(
            success=False,
            query=request.query,
            response="",
            workflow_id=request.workflow_id,
            execution_time=execution_time,
            error=str(e)
        )

@router.get("/history/{workflow_id}", response_model=List[ChatHistoryResponse])
def get_chat_history(
    workflow_id: int,
    session_id: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(ChatHistory).filter(ChatHistory.workflow_id == workflow_id)
    
    if session_id:
        query = query.filter(ChatHistory.session_id == session_id)
    
    history = query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    return history

@router.delete("/history/{chat_id}")
def delete_chat_history(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(ChatHistory).filter(ChatHistory.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat history not found")
    
    db.delete(chat)
    db.commit()
    
    return {"success": True, "message": "Chat history deleted successfully"}