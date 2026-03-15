from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TagCreate(BaseModel):
    name: str
    color: str = "#6366F1"

class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class TagResponse(BaseModel):
    id: str
    name: str
    color: str
    organization_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class TagListResponse(BaseModel):
    items: List[TagResponse]
    total: int
