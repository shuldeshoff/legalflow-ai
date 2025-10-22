from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class IntegrationBase(BaseModel):
    name: str
    type: str  # crm, telegram, payment, webhook
    is_active: bool = True
    config: Optional[Dict[str, Any]] = None


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class IntegrationResponse(IntegrationBase):
    id: int
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class IntegrationLogResponse(BaseModel):
    id: int
    integration_id: int
    event_type: str
    status: str
    request_data: Optional[Dict[str, Any]]
    response_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class WebhookPayload(BaseModel):
    event: str
    data: Dict[str, Any]


class TelegramChatResponse(BaseModel):
    id: int
    chat_id: str
    user_id: Optional[int]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    last_message_at: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(BaseModel):
    amount: int  # Amount in kopecks/cents
    currency: str = "RUB"
    description: Optional[str] = None
    client_id: Optional[int] = None
    return_url: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    client_id: Optional[int]
    amount: int
    currency: str
    status: str
    payment_system: str
    payment_id: str
    payment_url: Optional[str]
    description: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

