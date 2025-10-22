from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class KnowledgeBaseCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    source: Optional[str] = None


class KnowledgeBaseUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    source: Optional[str] = None


class KnowledgeBaseResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]
    source: Optional[str]
    embedding_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    category: Optional[str] = None


class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]
    score: float

