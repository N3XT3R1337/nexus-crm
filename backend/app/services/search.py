from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.models.contact import Contact
from app.models.company import Company
from app.models.deal import Deal
from app.schemas.common import SearchResult


async def full_text_search(
    db: AsyncSession, query: str, entity_types: list = None, page: int = 1, per_page: int = 25, organization_id: str = None
):
    results = []
    search_term = f"%{query.lower()}%"

    if not entity_types or "contact" in entity_types:
        stmt = select(Contact).where(
            or_(
                func.lower(Contact.first_name).like(search_term),
                func.lower(Contact.last_name).like(search_term),
                func.lower(Contact.email).like(search_term),
                func.lower(Contact.phone).like(search_term),
                func.lower(Contact.job_title).like(search_term),
            )
        )
        if organization_id:
            stmt = stmt.where(Contact.organization_id == organization_id)
        stmt = stmt.limit(per_page)
        res = await db.execute(stmt)
        for contact in res.scalars().all():
            score = 1.0
            if query.lower() in (contact.email or "").lower():
                score = 2.0
            results.append(SearchResult(
                entity_type="contact",
                entity_id=contact.id,
                title=f"{contact.first_name} {contact.last_name}",
                subtitle=contact.email,
                score=score,
            ))

    if not entity_types or "company" in entity_types:
        stmt = select(Company).where(
            or_(
                func.lower(Company.name).like(search_term),
                func.lower(Company.domain).like(search_term),
                func.lower(Company.industry).like(search_term),
                func.lower(Company.email).like(search_term),
            )
        )
        if organization_id:
            stmt = stmt.where(Company.organization_id == organization_id)
        stmt = stmt.limit(per_page)
        res = await db.execute(stmt)
        for company in res.scalars().all():
            results.append(SearchResult(
                entity_type="company",
                entity_id=company.id,
                title=company.name,
                subtitle=company.industry,
                score=1.0,
            ))

    if not entity_types or "deal" in entity_types:
        stmt = select(Deal).where(
            or_(
                func.lower(Deal.title).like(search_term),
                func.lower(Deal.description).like(search_term),
            )
        )
        if organization_id:
            stmt = stmt.where(Deal.organization_id == organization_id)
        stmt = stmt.limit(per_page)
        res = await db.execute(stmt)
        for deal in res.scalars().all():
            results.append(SearchResult(
                entity_type="deal",
                entity_id=deal.id,
                title=deal.title,
                subtitle=f"${deal.value:,.2f}",
                score=1.0,
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    total = len(results)
    start = (page - 1) * per_page
    return results[start:start + per_page], total
