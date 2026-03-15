import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class ContactStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEAD = "lead"
    CUSTOMER = "customer"
    CHURNED = "churned"


class ContactSource(str, enum.Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    COLD_CALL = "cold_call"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    EVENT = "event"
    OTHER = "other"


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    mobile: Mapped[str] = mapped_column(String(20), nullable=True)
    job_title: Mapped[str] = mapped_column(String(200), nullable=True)
    department: Mapped[str] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(SAEnum(ContactStatus), default=ContactStatus.LEAD)
    source: Mapped[str] = mapped_column(SAEnum(ContactSource), default=ContactSource.OTHER)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=True)
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=True)
    twitter_handle: Mapped[str] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=True)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="contacts")
    owner = relationship("User", back_populates="contacts", foreign_keys=[owner_id])
    deals = relationship("Deal", back_populates="contact")
    activities = relationship("Activity", back_populates="contact")
    notes = relationship("Note", back_populates="contact")
    tags = relationship("Tag", secondary="contact_tags", back_populates="contacts")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
