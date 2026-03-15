from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DealStageCreate(BaseModel):
    name: str
    order: int
    probability: float = 0.0
    color: str = "#3B82F6"

class DealStageUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    probability: Optional[float] = None
    color: Optional[str] = None

class DealStageResponse(BaseModel):
    id: str
    name: str
    order: int
    probability: float
    color: str
    organization_id: Optional[str] = None
    created_at: datetime
    model_config = {"from_attributes": True}

class DealCreate(BaseModel):
    title: str
    value: float = 0.0
    currency: str = "USD"
    priority: str = "medium"
    description: Optional[str] = None
    expected_close_date: Optional[datetime] = None
    stage_id: Optional[str] = None
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    tag_ids: Optional[List[str]] = None

class DealUpdate(BaseModel):
    title: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    description: Optional[str] = None
    expected_close_date: Optional[datetime] = None
    stage_id: Optional[str] = None
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    lost_reason: Optional[str] = None
    tag_ids: Optional[List[str]] = None

class DealResponse(BaseModel):
    id: str
    title: str
    value: float
    currency: str
    status: str
    priority: str
    description: Optional[str] = None
    expected_close_date: Optional[datetime] = None
    actual_close_date: Optional[datetime] = None
    probability: float
    stage_id: Optional[str] = None
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    organization_id: Optional[str] = None
    lost_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    stage: Optional[DealStageResponse] = None

    model_config = {"from_attributes": True}

class DealListResponse(BaseModel):
    items: List[DealResponse]
    total: int
    page: int
    per_page: int
    pages: int

class DealStageTransition(BaseModel):
    stage_id: str

class DealWin(BaseModel):
    actual_close_date: Optional[datetime] = None

class DealLose(BaseModel):
    lost_reason: str
