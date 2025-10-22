from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import (
    DocumentResponse,
    DocumentAnalysisResponse,
    DocumentAnalysisRequest
)
from app.services.document_processor import document_processor
from app.services.document_analyzer import document_analyzer
from app.services.vector_store import vector_store
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    client_id: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document (PDF, DOCX, TXT)
    
    File will be saved, text extracted, and prepared for analysis
    """
    try:
        # Validate file type
        try:
            file_type = document_processor.get_file_type(file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Save file
        file_path, file_size = await document_processor.save_file(file.file, file.filename)
        
        # Extract text
        try:
            extracted_text = document_processor.extract_text(file_path, file_type)
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            extracted_text = ""
        
        # Create database record
        db_document = Document(
            title=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            client_id=client_id,
            uploaded_by=current_user.id,
            extracted_text=extracted_text,
            analysis_status="pending"
        )
        
        db.add(db_document)
        await db.commit()
        await db.refresh(db_document)
        
        logger.info(f"Document uploaded: {db_document.id} - {file.filename}")
        
        return db_document
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{document_id}/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(
    document_id: int,
    analyze_risks: bool = True,
    analyze_key_points: bool = True,
    generate_summary: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze document using AI/LLM
    
    Extracts key points, identifies risks, and generates summary
    """
    try:
        # Get document
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if not document.extracted_text:
            raise HTTPException(status_code=400, detail="Document has no extracted text")
        
        # Update status
        document.analysis_status = "processing"
        await db.commit()
        
        # Analyze document
        try:
            analysis = await document_analyzer.analyze_document(
                text=document.extracted_text,
                title=document.title,
                analyze_risks=analyze_risks,
                analyze_key_points=analyze_key_points,
                generate_summary=generate_summary
            )
            
            # Update document with analysis results
            document.analysis_summary = analysis.get("summary")
            document.key_points = analysis.get("key_points")
            document.risks = analysis.get("risks")
            document.recommendations = analysis.get("recommendations")
            document.analysis_status = "completed"
            document.analyzed_at = datetime.utcnow()
            
            # Add to vector store for RAG
            if document.extracted_text:
                embedding_id = vector_store.add_document(
                    text=document.extracted_text,
                    metadata={
                        "title": document.title,
                        "category": "document",
                        "document_id": str(document.id),
                        "summary": document.analysis_summary or ""
                    }
                )
                document.embedding_id = embedding_id
            
            await db.commit()
            await db.refresh(document)
            
            logger.info(f"Document analyzed: {document_id}")
            
        except Exception as e:
            logger.error(f"Error analyzing document {document_id}: {e}")
            document.analysis_status = "failed"
            await db.commit()
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    client_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all documents"""
    try:
        query = select(Document)
        
        if client_id:
            query = query.where(Document.client_id == client_id)
        
        query = query.offset(skip).limit(limit).order_by(Document.uploaded_at.desc())
        
        result = await db.execute(query)
        documents = result.scalars().all()
        
        return documents
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentAnalysisResponse)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get document with analysis results"""
    try:
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete document"""
    try:
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete file from disk
        document_processor.delete_file(document.file_path)
        
        # Delete from vector store
        if document.embedding_id:
            try:
                vector_store.delete_document(document.embedding_id)
            except Exception as e:
                logger.warning(f"Error deleting from vector store: {e}")
        
        # Delete from database
        await db.delete(document)
        await db.commit()
        
        logger.info(f"Document deleted: {document_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

