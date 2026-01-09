from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentUploadResponse
from app.service.pdf_service import extract_text_from_pdf
from app.service.embedding_service import generate_embeddings, chunk_text
from app.service.vector_service import vector_service
from app.config import settings
import traceback
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        os.makedirs(settings.upload_dir, exist_ok=True)
        
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(settings.upload_dir, filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        file_size = len(content)
        
        collection_name = f"doc_{file_id}"
        
        document = Document(
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            status="processing",
            collection_name=collection_name
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        extraction_result = extract_text_from_pdf(file_path)
        
        if not extraction_result["success"]:
            document.status = "failed"
            document.error_message = extraction_result["error"]
            db.commit()
            return DocumentUploadResponse(
                success=False,
                message="Failed to extract text from PDF",
                error=extraction_result["error"]
            )

        document.content_preview = extraction_result["preview"]
        
        chunks = chunk_text(extraction_result["text"])
        
        embeddings = generate_embeddings(chunks)
        
        vector_service.add_documents(
            collection_name=collection_name,
            texts=chunks,
            embeddings=embeddings,
            metadatas=[{"document_id": document.id, "chunk_index": i} for i in range(len(chunks))]
        )
        
        document.status = "completed"
        db.commit()
        db.refresh(document)
        
        return DocumentUploadResponse(
            success=True,
            message="Document uploaded and processed successfully",
            document=DocumentResponse.from_orm(document)
        )
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        logger.error(traceback.format_exc())
        
        if 'document' in locals():
            document.status = "failed"
            document.error_message = str(e)
            db.commit()
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.created_at.desc()).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.collection_name:
        vector_service.delete_collection(document.collection_name)
    
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    
    return {"success": True, "message": "Document deleted successfully"}