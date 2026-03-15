from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 25
    sort_by: Optional[str] = None
    sort_order: str = "desc"

class SearchRequest(BaseModel):
    query: str
    entity_types: Optional[List[str]] = None
    page: int = 1
    per_page: int = 25

class SearchResult(BaseModel):
    entity_type: str
    entity_id: str
    title: str
    subtitle: Optional[str] = None
    score: float = 0.0

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str

class EmailTemplateCreate(BaseModel):
    name: str
    subject: str
    body: str
    category: Optional[str] = None
    variables: Optional[str] = None

class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    category: Optional[str] = None
    variables: Optional[str] = None

class EmailTemplateResponse(BaseModel):
    id: str
    name: str
    subject: str
    body: str
    category: Optional[str] = None
    variables: Optional[str] = None
    user_id: str
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    message: Optional[str] = None
    read: bool
    link: Optional[str] = None
    user_id: str
    created_at: datetime
    model_config = {"from_attributes": True}

class NotificationListResponse(BaseModel):
    items: List[NotificationResponse]
    total: int
    unread_count: int

class AuditLogResponse(BaseModel):
    id: str
    action: str
    entity_type: str
    entity_id: str
    changes: Optional[str] = None
    ip_address: Optional[str] = None
    user_id: str
    created_at: datetime
    model_config = {"from_attributes": True}

class AuditLogListResponse(BaseModel):
    items: List[AuditLogResponse]
    total: int
    page: int
    per_page: int

class WebhookCreate(BaseModel):
    name: str
    url: str
    secret: Optional[str] = None
    events: str
    is_active: bool = True

class WebhookUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    secret: Optional[str] = None
    events: Optional[str] = None
    is_active: Optional[bool] = None

class WebhookResponse(BaseModel):
    id: str
    name: str
    url: str
    events: str
    is_active: bool
    last_triggered_at: Optional[datetime] = None
    failure_count: int
    organization_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class ApiKeyCreate(BaseModel):
    name: str
    expires_at: Optional[datetime] = None

class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key: str
    is_active: bool
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    user_id: str
    created_at: datetime
    model_config = {"from_attributes": True}

class ReportCreate(BaseModel):
    name: str
    type: str
    config: Optional[str] = None
    is_public: bool = False

class ReportResponse(BaseModel):
    id: str
    name: str
    type: str
    config: Optional[str] = None
    data: Optional[str] = None
    is_public: bool
    user_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class DashboardStats(BaseModel):
    total_contacts: int
    total_companies: int
    total_deals: int
    total_revenue: float
    won_deals: int
    lost_deals: int
    open_deals: int
    conversion_rate: float
    avg_deal_value: float
    pipeline_value: float
    activities_this_week: int
    new_contacts_this_month: int

class RevenueForecaste(BaseModel):
    month: str
    predicted: float
    actual: float
    weighted: float

class PipelineVelocity(BaseModel):
    stage_name: str
    avg_days: float
    deal_count: int
    conversion_rate: float

class MessageResponse(BaseModel):
    message: str
    success: bool = True
