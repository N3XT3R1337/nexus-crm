from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.company import Company
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse, CompanyListResponse
from app.api.deps import get_current_user, require_perm
import json

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=CompanyListResponse)
async def list_companies(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    search: str = Query(None),
    industry: str = Query(None),
    size: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user: User = Depends(require_perm("companies:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Company)
    count_query = select(func.count(Company.id))

    if current_user.organization_id:
        query = query.where(Company.organization_id == current_user.organization_id)
        count_query = count_query.where(Company.organization_id == current_user.organization_id)

    if search:
        term = f"%{search}%"
        query = query.where((Company.name.ilike(term)) | (Company.domain.ilike(term)) | (Company.industry.ilike(term)))
        count_query = count_query.where((Company.name.ilike(term)) | (Company.domain.ilike(term)) | (Company.industry.ilike(term)))

    if industry:
        query = query.where(Company.industry == industry)
        count_query = count_query.where(Company.industry == industry)

    if size:
        query = query.where(Company.size == size)
        count_query = count_query.where(Company.size == size)

    total = await db.scalar(count_query) or 0
    sort_col = getattr(Company, sort_by, Company.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    offset = (page - 1) * per_page
    result = await db.execute(query.offset(offset).limit(per_page))
    companies = result.scalars().all()

    return CompanyListResponse(
        items=[CompanyResponse.model_validate(c) for c in companies],
        total=total, page=page, per_page=per_page,
        pages=(total + per_page - 1) // per_page if per_page else 0,
    )


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    current_user: User = Depends(require_perm("companies:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyResponse.model_validate(company)


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    data: CompanyCreate,
    current_user: User = Depends(require_perm("companies:write")),
    db: AsyncSession = Depends(get_db),
):
    company = Company(
        **data.model_dump(),
        owner_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(company)
    audit = AuditLog(
        action="create", entity_type="company", entity_id="pending",
        changes=json.dumps(data.model_dump()), user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.flush()
    audit.entity_id = company.id
    await db.refresh(company)
    return CompanyResponse.model_validate(company)


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    data: CompanyUpdate,
    current_user: User = Depends(require_perm("companies:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(company, key, value)

    audit = AuditLog(
        action="update", entity_type="company", entity_id=company_id,
        changes=json.dumps(update_data), user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.flush()
    await db.refresh(company)
    return CompanyResponse.model_validate(company)


@router.delete("/{company_id}")
async def delete_company(
    company_id: str,
    current_user: User = Depends(require_perm("companies:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    audit = AuditLog(
        action="delete", entity_type="company", entity_id=company_id,
        user_id=current_user.id, organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.delete(company)
    await db.flush()
    return {"message": "Company deleted", "success": True}


@router.get("/{company_id}/contacts")
async def get_company_contacts(
    company_id: str,
    current_user: User = Depends(require_perm("contacts:read")),
    db: AsyncSession = Depends(get_db),
):
    from app.models.contact import Contact
    from app.schemas.contact import ContactResponse
    result = await db.execute(select(Contact).where(Contact.company_id == company_id))
    contacts = result.scalars().all()
    return [ContactResponse.model_validate(c) for c in contacts]


@router.get("/{company_id}/deals")
async def get_company_deals(
    company_id: str,
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    from app.models.deal import Deal
    from app.schemas.deal import DealResponse
    result = await db.execute(select(Deal).where(Deal.company_id == company_id))
    deals = result.scalars().all()
    return [DealResponse.model_validate(d) for d in deals]
