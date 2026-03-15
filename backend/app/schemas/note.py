from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NoteCreate(BaseModel):
    content: str
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    company_id: Optional[str] = None

class NoteUpdate(BaseModel):
    content: Optional[str] = None

class NoteResponse(BaseModel):
    id: str
    content: str
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    company_id: Optional[str] = None
    user_id: str
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class NoteListResponse(BaseModel):
    items: List[NoteResponse]
    total: int
    page: int
    per_page: int
    pages: int
