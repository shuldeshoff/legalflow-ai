from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Integration(Base):
    """CRM and external integrations"""
    __tablename__ = "integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  # crm, telegram, payment, webhook
    is_active = Column(Boolean, default=True)
    
    # Configuration (JSON for flexibility)
    config = Column(JSON)  # API keys, endpoints, etc.
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IntegrationLog(Base):
    """Log of integration events"""
    __tablename__ = "integration_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    integration_id = Column(Integer, ForeignKey("integrations.id"))
    event_type = Column(String(100))  # webhook_received, message_sent, payment_received
    status = Column(String(50))  # success, failed, pending
    
    # Event data
    request_data = Column(JSON)
    response_data = Column(JSON)
    error_message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class TelegramChat(Base):
    """Telegram chat sessions"""
    __tablename__ = "telegram_chats"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Linked user
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    
    # Chat state
    is_active = Column(Boolean, default=True)
    last_message_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    """Payment transactions"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    
    # Payment details
    amount = Column(Integer, nullable=False)  # Amount in kopecks/cents
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")  # pending, succeeded, failed, canceled
    
    # External payment system
    payment_system = Column(String(50))  # yookassa, stripe
    payment_id = Column(String(200), unique=True)  # External payment ID
    payment_url = Column(String(500))  # Payment page URL
    
    # Metadata
    description = Column(Text)
    payment_metadata = Column(JSON)  # Renamed from metadata to avoid SQLAlchemy conflict
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

