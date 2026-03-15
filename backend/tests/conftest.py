import pytest
import asyncio
import os
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.contact import Contact, ContactStatus, ContactSource
from app.models.company import Company
from app.models.deal import Deal, DealStage, DealStatus, DealPriority
from app.models.activity import Activity, ActivityType
from app.models.note import Note
from app.models.tag import Tag

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture
async def db_session(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    from app.main import app

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def org(db_session):
    organization = Organization(name="Test Org", slug="test-org", domain="test.io")
    db_session.add(organization)
    await db_session.flush()
    await db_session.refresh(organization)
    return organization


@pytest.fixture
async def admin_user(db_session, org):
    user = User(
        email="admin@test.io",
        hashed_password=get_password_hash("admin123"),
        first_name="Admin",
        last_name="Test",
        role=UserRole.SUPER_ADMIN,
        organization_id=org.id,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def sales_user(db_session, org):
    user = User(
        email="sales@test.io",
        hashed_password=get_password_hash("sales123"),
        first_name="Sales",
        last_name="Rep",
        role=UserRole.SALES_REP,
        organization_id=org.id,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def viewer_user(db_session, org):
    user = User(
        email="viewer@test.io",
        hashed_password=get_password_hash("viewer123"),
        first_name="View",
        last_name="Only",
        role=UserRole.VIEWER,
        organization_id=org.id,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def admin_token(admin_user):
    return create_access_token({"sub": admin_user.id, "email": admin_user.email, "role": admin_user.role.value if hasattr(admin_user.role, "value") else admin_user.role})


@pytest.fixture
async def sales_token(sales_user):
    return create_access_token({"sub": sales_user.id, "email": sales_user.email, "role": sales_user.role.value if hasattr(sales_user.role, "value") else sales_user.role})


@pytest.fixture
async def viewer_token(viewer_user):
    return create_access_token({"sub": viewer_user.id, "email": viewer_user.email, "role": viewer_user.role.value if hasattr(viewer_user.role, "value") else viewer_user.role})


@pytest.fixture
async def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
async def sales_headers(sales_token):
    return {"Authorization": f"Bearer {sales_token}"}


@pytest.fixture
async def viewer_headers(viewer_token):
    return {"Authorization": f"Bearer {viewer_token}"}


@pytest.fixture
async def sample_company(db_session, org, admin_user):
    company = Company(
        name="Acme Corp",
        domain="acme.com",
        industry="Technology",
        size="51-200",
        revenue=5000000,
        owner_id=admin_user.id,
        organization_id=org.id,
    )
    db_session.add(company)
    await db_session.flush()
    await db_session.refresh(company)
    return company


@pytest.fixture
async def sample_contact(db_session, org, admin_user, sample_company):
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@acme.com",
        phone="+1234567890",
        status=ContactStatus.LEAD,
        source=ContactSource.WEBSITE,
        company_id=sample_company.id,
        owner_id=admin_user.id,
        organization_id=org.id,
    )
    db_session.add(contact)
    await db_session.flush()
    await db_session.refresh(contact)
    return contact


@pytest.fixture
async def sample_stages(db_session, org):
    stages_data = [
        {"name": "Lead", "order": 1, "probability": 10.0, "color": "#8B5CF6"},
        {"name": "Qualified", "order": 2, "probability": 25.0, "color": "#3B82F6"},
        {"name": "Proposal", "order": 3, "probability": 50.0, "color": "#F59E0B"},
        {"name": "Negotiation", "order": 4, "probability": 75.0, "color": "#F97316"},
        {"name": "Closed Won", "order": 5, "probability": 100.0, "color": "#10B981"},
        {"name": "Closed Lost", "order": 6, "probability": 0.0, "color": "#EF4444"},
    ]
    stages = []
    for data in stages_data:
        stage = DealStage(**data, organization_id=org.id)
        db_session.add(stage)
        stages.append(stage)
    await db_session.flush()
    for s in stages:
        await db_session.refresh(s)
    return stages


@pytest.fixture
async def sample_deal(db_session, org, admin_user, sample_contact, sample_company, sample_stages):
    deal = Deal(
        title="Big Enterprise Deal",
        value=50000,
        currency="USD",
        status=DealStatus.OPEN,
        priority=DealPriority.HIGH,
        probability=sample_stages[0].probability,
        stage_id=sample_stages[0].id,
        contact_id=sample_contact.id,
        company_id=sample_company.id,
        owner_id=admin_user.id,
        organization_id=org.id,
    )
    db_session.add(deal)
    await db_session.flush()
    await db_session.refresh(deal)
    return deal


@pytest.fixture
async def sample_tag(db_session, org):
    tag = Tag(name="VIP", color="#EF4444", organization_id=org.id)
    db_session.add(tag)
    await db_session.flush()
    await db_session.refresh(tag)
    return tag
