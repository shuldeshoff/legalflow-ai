from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class DocumentBase(BaseModel):
    title: str
    client_id: Optional[int] = None


class DocumentUpload(BaseModel):
    client_id: Optional[int] = None


class DocumentResponse(BaseModel):
    id: int
    title: str
    file_path: str
    file_type: Optional[str]
    file_size: Optional[int]
    uploaded_at: datetime
    client_id: Optional[int]
    uploaded_by: Optional[int]
    analysis_status: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)


class DocumentAnalysisResponse(BaseModel):
    id: int
    title: str
    analysis_status: str
    analysis_summary: Optional[str]
    key_points: Optional[List[str]]
    risks: Optional[List[dict]]
    recommendations: Optional[str]
    analyzed_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


class DocumentAnalysisRequest(BaseModel):
    document_id: int
    analyze_risks: bool = True
    analyze_key_points: bool = True
    generate_summary: bool = True

