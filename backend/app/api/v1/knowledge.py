from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User
from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse,
    SearchRequest,
    SearchResult
)
from app.services.vector_store import vector_store
from app.services.rag_service import rag_service
from app.schemas.llm import LLMModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge(
    knowledge: KnowledgeBaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new knowledge base entry (Admin only)"""
    try:
        # Add to vector store
        embedding_id = vector_store.add_document(
            text=knowledge.content,
            metadata={
                "title": knowledge.title,
                "category": knowledge.category or "",
                "source": knowledge.source or ""
            }
        )
        
        # Save to database
        db_knowledge = KnowledgeBase(
            title=knowledge.title,
            content=knowledge.content,
            category=knowledge.category,
            source=knowledge.source,
            embedding_id=embedding_id,
            created_by=current_user.id
        )
        
        db.add(db_knowledge)
        await db.commit()
        await db.refresh(db_knowledge)
        
        return db_knowledge
        
    except Exception as e:
        logger.error(f"Error creating knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[KnowledgeBaseResponse])
async def list_knowledge(
    skip: int = 0,
    limit: int = 20,
    category: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all knowledge base entries"""
    try:
        query = select(KnowledgeBase)
        
        if category:
            query = query.where(KnowledgeBase.category == category)
        
        query = query.offset(skip).limit(limit).order_by(KnowledgeBase.created_at.desc())
        
        result = await db.execute(query)
        knowledge = result.scalars().all()
        
        return knowledge
        
    except Exception as e:
        logger.error(f"Error listing knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{knowledge_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge(
    knowledge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get knowledge base entry by ID"""
    try:
        result = await db.execute(
            select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
        )
        knowledge = result.scalar_one_or_none()
        
        if not knowledge:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        return knowledge
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{knowledge_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge(
    knowledge_id: int,
    knowledge_update: KnowledgeBaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update knowledge base entry (Admin only)"""
    try:
        result = await db.execute(
            select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
        )
        knowledge = result.scalar_one_or_none()
        
        if not knowledge:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        # Update fields
        update_data = knowledge_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(knowledge, field, value)
        
        # Update in vector store if content changed
        if knowledge_update.content:
            vector_store.update_document(
                doc_id=knowledge.embedding_id,
                text=knowledge.content,
                metadata={
                    "title": knowledge.title,
                    "category": knowledge.category or "",
                    "source": knowledge.source or ""
                }
            )
        
        await db.commit()
        await db.refresh(knowledge)
        
        return knowledge
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge(
    knowledge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete knowledge base entry (Admin only)"""
    try:
        result = await db.execute(
            select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
        )
        knowledge = result.scalar_one_or_none()
        
        if not knowledge:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        
        # Delete from vector store
        vector_store.delete_document(knowledge.embedding_id)
        
        # Delete from database
        await db.delete(knowledge)
        await db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResult])
async def search_knowledge(
    search: SearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search knowledge base using semantic search"""
    try:
        where = {"category": search.category} if search.category else None
        
        results = vector_store.search(
            query=search.query,
            n_results=search.limit,
            where=where
        )
        
        return [
            SearchResult(
                id=0,  # We don't have DB ID here
                title=result['metadata'].get('title', ''),
                content=result['text'],
                category=result['metadata'].get('category'),
                score=1 - result['distance']  # Convert distance to similarity score
            )
            for result in results
        ]
        
    except Exception as e:
        logger.error(f"Error searching knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag")
async def rag_query(
    search: SearchRequest,
    model: LLMModel = LLMModel.GPT_35_TURBO,
    current_user: User = Depends(get_current_user)
):
    """
    Ask question with RAG (Retrieval Augmented Generation)
    
    Returns answer generated by LLM using relevant context from knowledge base
    """
    try:
        result = await rag_service.generate_with_context(
            query=search.query,
            model=model,
            n_results=search.limit,
            category=search.category
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in RAG query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get knowledge base statistics"""
    try:
        # Database stats
        result = await db.execute(select(func.count(KnowledgeBase.id)))
        total_db = result.scalar()
        
        # Category counts
        result = await db.execute(
            select(KnowledgeBase.category, func.count(KnowledgeBase.id))
            .group_by(KnowledgeBase.category)
        )
        categories = {cat: count for cat, count in result.all()}
        
        # Vector store stats
        vector_stats = vector_store.get_stats()
        
        return {
            "total_documents": total_db,
            "categories": categories,
            "vector_store": vector_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

