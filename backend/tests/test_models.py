import pytest
from app.models.user import User, UserRole
from app.models.contact import Contact, ContactStatus
from app.models.company import Company
from app.models.deal import Deal, DealStatus, DealPriority
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token


def test_user_role_enum():
    assert UserRole.SUPER_ADMIN.value == "super_admin"
    assert UserRole.ADMIN.value == "admin"
    assert UserRole.MANAGER.value == "manager"
    assert UserRole.SALES_REP.value == "sales_rep"
    assert UserRole.VIEWER.value == "viewer"


def test_contact_status_enum():
    assert ContactStatus.ACTIVE.value == "active"
    assert ContactStatus.LEAD.value == "lead"
    assert ContactStatus.CUSTOMER.value == "customer"


def test_deal_status_enum():
    assert DealStatus.OPEN.value == "open"
    assert DealStatus.WON.value == "won"
    assert DealStatus.LOST.value == "lost"


def test_password_hashing():
    password = "securepassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_access_token():
    data = {"sub": "user-123", "email": "test@test.io", "role": "admin"}
    token = create_access_token(data)
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["email"] == "test@test.io"
    assert payload["type"] == "access"


def test_invalid_token():
    payload = decode_token("invalid.token.here")
    assert payload is None


def test_deal_priority_enum():
    assert DealPriority.LOW.value == "low"
    assert DealPriority.CRITICAL.value == "critical"
