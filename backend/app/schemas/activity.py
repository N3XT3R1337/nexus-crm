from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ActivityCreate(BaseModel):
    type: str
    subject: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None

class ActivityUpdate(BaseModel):
    type: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None

class ActivityResponse(BaseModel):
    id: str
    type: str
    subject: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    user_id: str
    contact_id: Optional[str] = None
    deal_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ActivityListResponse(BaseModel):
    items: List[ActivityResponse]
    total: int
    page: int
    per_page: int
    pages: int
