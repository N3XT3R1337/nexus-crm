from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    status: str = "lead"
    source: str = "other"
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    company_id: Optional[str] = None
    tag_ids: Optional[List[str]] = None

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    tag_ids: Optional[List[str]] = None

class TagBrief(BaseModel):
    id: str
    name: str
    color: str
    model_config = {"from_attributes": True}

class CompanyBrief(BaseModel):
    id: str
    name: str
    model_config = {"from_attributes": True}

class ContactResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    status: str
    source: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    avatar_url: Optional[str] = None
    company_id: Optional[str] = None
    owner_id: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagBrief] = []
    company: Optional[CompanyBrief] = None

    model_config = {"from_attributes": True}

class ContactListResponse(BaseModel):
    items: List[ContactResponse]
    total: int
    page: int
    per_page: int
    pages: int

class BulkContactAction(BaseModel):
    ids: List[str]
    action: str
    value: Optional[str] = None
