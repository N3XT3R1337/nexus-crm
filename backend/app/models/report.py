import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum


class ReportType(str, enum.Enum):
    SALES_PIPELINE = "sales_pipeline"
    REVENUE_FORECAST = "revenue_forecast"
    ACTIVITY_SUMMARY = "activity_summary"
    CONVERSION_RATE = "conversion_rate"
    DEAL_VELOCITY = "deal_velocity"
    TEAM_PERFORMANCE = "team_performance"
    CUSTOM = "custom"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(SAEnum(ReportType), nullable=False)
    config: Mapped[str] = mapped_column(Text, nullable=True)
    data: Mapped[str] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
