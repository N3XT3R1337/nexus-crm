import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


contact_tags = Table(
    "contact_tags",
    Base.metadata,
    Column("contact_id", String(36), ForeignKey("contacts.id"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id"), primary_key=True),
)

deal_tags = Table(
    "deal_tags",
    Base.metadata,
    Column("deal_id", String(36), ForeignKey("deals.id"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id"), primary_key=True),
)

company_tags = Table(
    "company_tags",
    Base.metadata,
    Column("company_id", String(36), ForeignKey("companies.id"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    color: Mapped[str] = mapped_column(String(7), default="#6366F1")
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    contacts = relationship("Contact", secondary=contact_tags, back_populates="tags")
    deals = relationship("Deal", secondary=deal_tags, back_populates="tags")
    companies = relationship("Company", secondary=company_tags, back_populates="tags")
