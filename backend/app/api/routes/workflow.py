from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import time

from app.database import get_db
from app.models.workflow import Workflow
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowValidateRequest,
    WorkflowValidateResponse,
    WorkflowExecuteRequest,
    WorkflowExecuteResponse
)
from app.core.validator import validate_workflow
from app.service.workflow_executor import execute_workflow

router = APIRouter(prefix="/workflow", tags=["workflow"])

@router.post("/validate", response_model=WorkflowValidateResponse)
def validate_workflow_route(request: WorkflowValidateRequest):
    nodes = [node.dict() for node in request.nodes]
    edges = [edge.dict() for edge in request.edges]
    
    is_valid, message = validate_workflow(nodes, edges)
    
    return WorkflowValidateResponse(
        valid=is_valid,
        message=message
    )

@router.post("/execute", response_model=WorkflowExecuteResponse)
def execute_workflow_route(request: WorkflowExecuteRequest):
    start_time = time.time()
    
    nodes = [node.dict() for node in request.nodes]
    edges = [edge.dict() for edge in request.edges]
    
    result = execute_workflow(nodes, edges, request.query)
    
    execution_time = int((time.time() - start_time) * 1000)
    
    if result.get("success"):
        return WorkflowExecuteResponse(
            success=True,
            query=request.query,
            response=result.get("response", ""),
            execution_log=result.get("execution_log", []),
            metadata={
                **result.get("metadata", {}),
                "execution_time_ms": execution_time
            }
        )
    else:
        return WorkflowExecuteResponse(
            success=False,
            query=request.query,
            response="",
            execution_log=result.get("execution_log", []),
            error=result.get("error", "Unknown error")
        )

@router.post("/save", response_model=WorkflowResponse)
def save_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    nodes = [node.dict() for node in workflow.nodes]
    edges = [edge.dict() for edge in workflow.edges]
    
    is_valid, message = validate_workflow(nodes, edges)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid workflow: {message}")
    
    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        nodes=nodes,
        edges=edges,
        config=workflow.config or {},
        status="draft"
    )
    
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    
    return db_workflow

@router.get("/", response_model=List[WorkflowResponse])
def list_workflows(db: Session = Depends(get_db)):
    workflows = db.query(Workflow).order_by(Workflow.created_at.desc()).all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow_update.name is not None:
        workflow.name = workflow_update.name
    if workflow_update.description is not None:
        workflow.description = workflow_update.description
    if workflow_update.nodes is not None:
        workflow.nodes = [node.dict() for node in workflow_update.nodes]
    if workflow_update.edges is not None:
        workflow.edges = [edge.dict() for edge in workflow_update.edges]
    if workflow_update.config is not None:
        workflow.config = workflow_update.config
    if workflow_update.status is not None:
        workflow.status = workflow_update.status
    
    db.commit()
    db.refresh(workflow)
    
    return workflow

@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    db.delete(workflow)
    db.commit()
    
    return {"success": True, "message": "Workflow deleted successfully"}