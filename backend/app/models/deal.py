import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class DealPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DealStatus(str, enum.Enum):
    OPEN = "open"
    WON = "won"
    LOST = "lost"
    ABANDONED = "abandoned"


class DealStage(Base):
    __tablename__ = "deal_stages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    probability: Mapped[float] = mapped_column(Float, default=0.0)
    color: Mapped[str] = mapped_column(String(7), default="#3B82F6")
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    deals = relationship("Deal", back_populates="stage")


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    status: Mapped[str] = mapped_column(SAEnum(DealStatus), default=DealStatus.OPEN)
    priority: Mapped[str] = mapped_column(SAEnum(DealPriority), default=DealPriority.MEDIUM)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    expected_close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    actual_close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    probability: Mapped[float] = mapped_column(Float, default=0.0)
    stage_id: Mapped[str] = mapped_column(String(36), ForeignKey("deal_stages.id"), nullable=True)
    contact_id: Mapped[str] = mapped_column(String(36), ForeignKey("contacts.id"), nullable=True)
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=True)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=True)
    lost_reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    stage = relationship("DealStage", back_populates="deals")
    contact = relationship("Contact", back_populates="deals")
    company = relationship("Company", back_populates="deals")
    owner = relationship("User", back_populates="deals", foreign_keys=[owner_id])
    activities = relationship("Activity", back_populates="deal")
    notes = relationship("Note", back_populates="deal")
    tags = relationship("Tag", secondary="deal_tags", back_populates="deals")
