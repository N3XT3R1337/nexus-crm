import asyncio
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base
from app.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.contact import Contact, ContactStatus, ContactSource
from app.models.company import Company
from app.models.deal import Deal, DealStage, DealStatus, DealPriority
from app.models.activity import Activity, ActivityType
from app.models.note import Note
from app.models.tag import Tag
from app.models.email_template import EmailTemplate
from app.models.notification import Notification, NotificationType

fake = Faker()

INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Manufacturing", "Retail",
    "Education", "Real Estate", "Consulting", "Media", "Energy",
    "Transportation", "Agriculture", "Telecommunications", "Hospitality", "Legal",
]

COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]

TAG_DATA = [
    {"name": "VIP", "color": "#EF4444"},
    {"name": "Enterprise", "color": "#8B5CF6"},
    {"name": "SMB", "color": "#3B82F6"},
    {"name": "Hot Lead", "color": "#F97316"},
    {"name": "Cold Lead", "color": "#6B7280"},
    {"name": "Partner", "color": "#10B981"},
    {"name": "Referral", "color": "#F59E0B"},
    {"name": "Churned", "color": "#EF4444"},
    {"name": "Upsell", "color": "#8B5CF6"},
    {"name": "Cross-sell", "color": "#3B82F6"},
    {"name": "Priority", "color": "#EC4899"},
    {"name": "Follow-up", "color": "#14B8A6"},
]

STAGE_DATA = [
    {"name": "Lead", "order": 1, "probability": 10.0, "color": "#8B5CF6"},
    {"name": "Qualified", "order": 2, "probability": 25.0, "color": "#3B82F6"},
    {"name": "Proposal", "order": 3, "probability": 50.0, "color": "#F59E0B"},
    {"name": "Negotiation", "order": 4, "probability": 75.0, "color": "#F97316"},
    {"name": "Closed Won", "order": 5, "probability": 100.0, "color": "#10B981"},
    {"name": "Closed Lost", "order": 6, "probability": 0.0, "color": "#EF4444"},
]

EMAIL_TEMPLATES = [
    {"name": "Welcome Email", "subject": "Welcome to {{company_name}}", "body": "<h1>Welcome!</h1><p>Dear {{contact_name}},</p><p>Welcome aboard!</p>", "category": "onboarding"},
    {"name": "Follow-up", "subject": "Following up on our conversation", "body": "<p>Dear {{contact_name}},</p><p>I wanted to follow up on our recent conversation.</p>", "category": "sales"},
    {"name": "Proposal", "subject": "Proposal for {{deal_title}}", "body": "<p>Dear {{contact_name}},</p><p>Please find attached our proposal.</p>", "category": "sales"},
    {"name": "Thank You", "subject": "Thank you for choosing us", "body": "<p>Dear {{contact_name}},</p><p>Thank you for your business!</p>", "category": "post-sale"},
    {"name": "Meeting Request", "subject": "Meeting Request: {{subject}}", "body": "<p>Dear {{contact_name}},</p><p>I would like to schedule a meeting.</p>", "category": "scheduling"},
]


async def seed_database():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        org = Organization(name="Nexus Corp", slug="nexus-corp", domain="nexuscorp.io", plan="enterprise", max_users=100)
        session.add(org)
        await session.flush()

        admin = User(
            email=settings.DEFAULT_ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            first_name="Admin",
            last_name="User",
            role=UserRole.SUPER_ADMIN,
            organization_id=org.id,
        )
        session.add(admin)

        users = [admin]
        team_members = [
            ("Sarah", "Johnson", UserRole.ADMIN),
            ("Michael", "Chen", UserRole.MANAGER),
            ("Emily", "Davis", UserRole.SALES_REP),
            ("James", "Wilson", UserRole.SALES_REP),
            ("Jessica", "Martinez", UserRole.SALES_REP),
            ("David", "Brown", UserRole.SALES_REP),
            ("Amanda", "Taylor", UserRole.MANAGER),
            ("Robert", "Anderson", UserRole.VIEWER),
            ("Lisa", "Thomas", UserRole.SALES_REP),
        ]

        for first, last, role in team_members:
            user = User(
                email=f"{first.lower()}.{last.lower()}@nexuscorp.io",
                hashed_password=get_password_hash("password123"),
                first_name=first,
                last_name=last,
                role=role,
                organization_id=org.id,
            )
            session.add(user)
            users.append(user)

        await session.flush()

        tags = []
        for tag_data in TAG_DATA:
            tag = Tag(name=tag_data["name"], color=tag_data["color"], organization_id=org.id)
            session.add(tag)
            tags.append(tag)
        await session.flush()

        stages = []
        for stage_data in STAGE_DATA:
            stage = DealStage(
                name=stage_data["name"],
                order=stage_data["order"],
                probability=stage_data["probability"],
                color=stage_data["color"],
                organization_id=org.id,
            )
            session.add(stage)
            stages.append(stage)
        await session.flush()

        companies = []
        for i in range(200):
            company = Company(
                name=fake.company(),
                domain=fake.domain_name(),
                industry=random.choice(INDUSTRIES),
                size=random.choice(COMPANY_SIZES),
                revenue=round(random.uniform(100000, 50000000), 2),
                phone=fake.phone_number()[:20],
                email=fake.company_email(),
                website=fake.url(),
                description=fake.catch_phrase(),
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state_abbr(),
                country="US",
                zip_code=fake.zipcode(),
                employee_count=random.randint(5, 5000),
                founded_year=random.randint(1990, 2024),
                owner_id=random.choice(users).id,
                organization_id=org.id,
            )
            session.add(company)
            companies.append(company)
        await session.flush()

        contacts = []
        statuses = list(ContactStatus)
        sources = list(ContactSource)
        for i in range(500):
            contact = Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number()[:20],
                mobile=fake.phone_number()[:20] if random.random() > 0.3 else None,
                job_title=fake.job()[:200],
                department=random.choice(["Sales", "Marketing", "Engineering", "HR", "Finance", "Operations", "Support"]),
                status=random.choice(statuses),
                source=random.choice(sources),
                address=fake.street_address() if random.random() > 0.5 else None,
                city=fake.city(),
                state=fake.state_abbr(),
                country="US",
                zip_code=fake.zipcode(),
                company_id=random.choice(companies).id if random.random() > 0.2 else None,
                owner_id=random.choice(users).id,
                organization_id=org.id,
            )
            session.add(contact)
            contacts.append(contact)
        await session.flush()

        for contact in contacts:
            num_tags = random.randint(0, 3)
            if num_tags > 0:
                contact.tags = random.sample(tags, min(num_tags, len(tags)))

        open_stages = [s for s in stages if s.name not in ("Closed Won", "Closed Lost")]
        won_stage = next((s for s in stages if s.name == "Closed Won"), stages[-2])
        lost_stage = next((s for s in stages if s.name == "Closed Lost"), stages[-1])
        priorities = list(DealPriority)

        deals = []
        for i in range(100):
            is_won = random.random() < 0.3
            is_lost = random.random() < 0.15 if not is_won else False

            if is_won:
                deal_stage = won_stage
                deal_status = DealStatus.WON
            elif is_lost:
                deal_stage = lost_stage
                deal_status = DealStatus.LOST
            else:
                deal_stage = random.choice(open_stages)
                deal_status = DealStatus.OPEN

            created = fake.date_time_between(start_date="-6M", end_date="now")
            deal = Deal(
                title=f"{fake.bs().title()} - {fake.company()}",
                value=round(random.uniform(1000, 500000), 2),
                currency="USD",
                status=deal_status,
                priority=random.choice(priorities),
                description=fake.paragraph(nb_sentences=3),
                expected_close_date=created + timedelta(days=random.randint(14, 180)),
                actual_close_date=created + timedelta(days=random.randint(7, 90)) if deal_status != DealStatus.OPEN else None,
                probability=deal_stage.probability,
                stage_id=deal_stage.id,
                contact_id=random.choice(contacts).id if random.random() > 0.1 else None,
                company_id=random.choice(companies).id if random.random() > 0.2 else None,
                owner_id=random.choice(users).id,
                organization_id=org.id,
                lost_reason=fake.sentence() if is_lost else None,
                created_at=created,
            )
            session.add(deal)
            deals.append(deal)
        await session.flush()

        activity_types = list(ActivityType)
        for i in range(300):
            created = fake.date_time_between(start_date="-3M", end_date="now")
            is_completed = random.random() > 0.4
            activity = Activity(
                type=random.choice(activity_types),
                subject=fake.sentence(nb_words=6)[:300],
                description=fake.paragraph(nb_sentences=2) if random.random() > 0.3 else None,
                due_date=created + timedelta(days=random.randint(0, 14)),
                completed=is_completed,
                completed_at=created + timedelta(hours=random.randint(1, 48)) if is_completed else None,
                duration_minutes=random.choice([15, 30, 45, 60, 90, 120]) if random.random() > 0.5 else None,
                user_id=random.choice(users).id,
                contact_id=random.choice(contacts).id if random.random() > 0.3 else None,
                deal_id=random.choice(deals).id if random.random() > 0.5 else None,
                organization_id=org.id,
                created_at=created,
            )
            session.add(activity)

        for i in range(200):
            note = Note(
                content=fake.paragraph(nb_sentences=random.randint(1, 5)),
                contact_id=random.choice(contacts).id if random.random() > 0.3 else None,
                deal_id=random.choice(deals).id if random.random() > 0.5 else None,
                company_id=random.choice(companies).id if random.random() > 0.7 else None,
                user_id=random.choice(users).id,
                organization_id=org.id,
            )
            session.add(note)

        for tmpl in EMAIL_TEMPLATES:
            et = EmailTemplate(
                name=tmpl["name"],
                subject=tmpl["subject"],
                body=tmpl["body"],
                category=tmpl["category"],
                variables="contact_name,company_name,deal_title,subject",
                user_id=admin.id,
                organization_id=org.id,
            )
            session.add(et)

        notification_types = list(NotificationType)
        for i in range(50):
            notification = Notification(
                type=random.choice(notification_types),
                title=fake.sentence(nb_words=5),
                message=fake.sentence(nb_words=10),
                read=random.random() > 0.5,
                link=f"/deals/{random.choice(deals).id}" if random.random() > 0.5 else None,
                user_id=random.choice(users).id,
                organization_id=org.id,
            )
            session.add(notification)

        await session.commit()
        print(f"Seeded: {len(users)} users, {len(companies)} companies, {len(contacts)} contacts, {len(deals)} deals")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
