from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, BigInteger
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class DocumentType(str, enum.Enum):
    CONTRACT = "contract"
    CLAIM = "claim"
    COMPLAINT = "complaint"
    OTHER = "other"


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    type = Column(SQLEnum(DocumentType), default=DocumentType.OTHER)
    file_path = Column(String(500), nullable=False)
    original_name = Column(String(255), nullable=False)
    mime_type = Column(String(100))
    size = Column(BigInteger)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="documents")

