from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    phone: Optional[str] = None
    telegram_id: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    user_id: Optional[int] = None


class ClientUpdate(ClientBase):
    status: Optional[str] = None


class ClientResponse(ClientBase):
    id: int
    user_id: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

