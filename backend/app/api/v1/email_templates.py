from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.email_template import EmailTemplate
from app.models.user import User
from app.schemas.common import EmailTemplateCreate, EmailTemplateUpdate, EmailTemplateResponse
from app.api.deps import get_current_user, require_perm

router = APIRouter(prefix="/email-templates", tags=["Email Templates"])


@router.get("")
async def list_templates(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    category: str = Query(None),
    search: str = Query(None),
    current_user: User = Depends(require_perm("email_templates:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(EmailTemplate)
    count_query = select(func.count(EmailTemplate.id))

    if current_user.organization_id:
        query = query.where(EmailTemplate.organization_id == current_user.organization_id)
        count_query = count_query.where(EmailTemplate.organization_id == current_user.organization_id)

    if category:
        query = query.where(EmailTemplate.category == category)
        count_query = count_query.where(EmailTemplate.category == category)

    if search:
        term = f"%{search}%"
        query = query.where(EmailTemplate.name.ilike(term))
        count_query = count_query.where(EmailTemplate.name.ilike(term))

    total = await db.scalar(count_query) or 0
    offset = (page - 1) * per_page
    result = await db.execute(query.order_by(EmailTemplate.created_at.desc()).offset(offset).limit(per_page))
    templates = result.scalars().all()

    return {
        "items": [EmailTemplateResponse.model_validate(t) for t in templates],
        "total": total, "page": page, "per_page": per_page,
    }


@router.get("/{template_id}", response_model=EmailTemplateResponse)
async def get_template(
    template_id: str,
    current_user: User = Depends(require_perm("email_templates:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id))
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return EmailTemplateResponse.model_validate(template)


@router.post("", response_model=EmailTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    data: EmailTemplateCreate,
    current_user: User = Depends(require_perm("email_templates:write")),
    db: AsyncSession = Depends(get_db),
):
    template = EmailTemplate(
        **data.model_dump(),
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(template)
    await db.flush()
    await db.refresh(template)
    return EmailTemplateResponse.model_validate(template)


@router.put("/{template_id}", response_model=EmailTemplateResponse)
async def update_template(
    template_id: str,
    data: EmailTemplateUpdate,
    current_user: User = Depends(require_perm("email_templates:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id))
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(template, key, value)
    await db.flush()
    await db.refresh(template)
    return EmailTemplateResponse.model_validate(template)


@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    current_user: User = Depends(require_perm("email_templates:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id))
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    await db.delete(template)
    await db.flush()
    return {"message": "Template deleted", "success": True}
