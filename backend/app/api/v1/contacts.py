from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.contact import Contact
from app.models.tag import Tag
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse, ContactListResponse, BulkContactAction
from app.api.deps import get_current_user, require_perm
import json

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=ContactListResponse)
async def list_contacts(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    search: str = Query(None),
    status_filter: str = Query(None, alias="status"),
    source: str = Query(None),
    company_id: str = Query(None),
    owner_id: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user: User = Depends(require_perm("contacts:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Contact).options(selectinload(Contact.tags), selectinload(Contact.company))
    count_query = select(func.count(Contact.id))

    if current_user.organization_id:
        query = query.where(Contact.organization_id == current_user.organization_id)
        count_query = count_query.where(Contact.organization_id == current_user.organization_id)

    if search:
        term = f"%{search}%"
        query = query.where(
            (Contact.first_name.ilike(term)) | (Contact.last_name.ilike(term)) |
            (Contact.email.ilike(term)) | (Contact.phone.ilike(term))
        )
        count_query = count_query.where(
            (Contact.first_name.ilike(term)) | (Contact.last_name.ilike(term)) |
            (Contact.email.ilike(term)) | (Contact.phone.ilike(term))
        )

    if status_filter:
        query = query.where(Contact.status == status_filter)
        count_query = count_query.where(Contact.status == status_filter)

    if source:
        query = query.where(Contact.source == source)
        count_query = count_query.where(Contact.source == source)

    if company_id:
        query = query.where(Contact.company_id == company_id)
        count_query = count_query.where(Contact.company_id == company_id)

    if owner_id:
        query = query.where(Contact.owner_id == owner_id)
        count_query = count_query.where(Contact.owner_id == owner_id)

    total = await db.scalar(count_query) or 0

    sort_col = getattr(Contact, sort_by, Contact.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    offset = (page - 1) * per_page
    result = await db.execute(query.offset(offset).limit(per_page))
    contacts = result.scalars().all()

    return ContactListResponse(
        items=[ContactResponse.model_validate(c) for c in contacts],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page if per_page else 0,
    )


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: str,
    current_user: User = Depends(require_perm("contacts:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contact).options(selectinload(Contact.tags), selectinload(Contact.company)).where(Contact.id == contact_id)
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse.model_validate(contact)


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    data: ContactCreate,
    current_user: User = Depends(require_perm("contacts:write")),
    db: AsyncSession = Depends(get_db),
):
    contact = Contact(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        mobile=data.mobile,
        job_title=data.job_title,
        department=data.department,
        status=data.status,
        source=data.source,
        address=data.address,
        city=data.city,
        state=data.state,
        country=data.country,
        zip_code=data.zip_code,
        linkedin_url=data.linkedin_url,
        twitter_handle=data.twitter_handle,
        company_id=data.company_id,
        owner_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(contact)
    await db.flush()

    if data.tag_ids:
        tag_result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
        contact.tags = list(tag_result.scalars().all())

    audit = AuditLog(
        action="create",
        entity_type="contact",
        entity_id=contact.id,
        changes=json.dumps(data.model_dump()),
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.flush()
    fresh = await db.execute(
        select(Contact).options(selectinload(Contact.tags), selectinload(Contact.company)).where(Contact.id == contact.id)
    )
    contact = fresh.scalar_one()
    return ContactResponse.model_validate(contact)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str,
    data: ContactUpdate,
    current_user: User = Depends(require_perm("contacts:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contact).options(selectinload(Contact.tags), selectinload(Contact.company)).where(Contact.id == contact_id)
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    update_data = data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    for key, value in update_data.items():
        setattr(contact, key, value)

    if tag_ids is not None:
        tag_result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        contact.tags = list(tag_result.scalars().all())

    audit = AuditLog(
        action="update",
        entity_type="contact",
        entity_id=contact.id,
        changes=json.dumps(update_data),
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.flush()
    fresh = await db.execute(
        select(Contact).options(selectinload(Contact.tags), selectinload(Contact.company)).where(Contact.id == contact.id)
    )
    contact = fresh.scalar_one()
    return ContactResponse.model_validate(contact)


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: str,
    current_user: User = Depends(require_perm("contacts:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    audit = AuditLog(
        action="delete",
        entity_type="contact",
        entity_id=contact.id,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(audit)
    await db.delete(contact)
    await db.flush()
    return {"message": "Contact deleted", "success": True}


@router.post("/bulk")
async def bulk_contact_action(
    data: BulkContactAction,
    current_user: User = Depends(require_perm("contacts:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Contact).where(Contact.id.in_(data.ids)))
    contacts = result.scalars().all()

    if data.action == "delete":
        from app.core.rbac import check_permission
        if not check_permission(current_user.role, "contacts:bulk_delete"):
            raise HTTPException(status_code=403, detail="Insufficient permissions for bulk delete")
        for contact in contacts:
            await db.delete(contact)
    elif data.action == "assign":
        for contact in contacts:
            contact.owner_id = data.value
    elif data.action == "change_status":
        for contact in contacts:
            contact.status = data.value
    elif data.action == "add_tag":
        tag_result = await db.execute(select(Tag).where(Tag.id == data.value))
        tag = tag_result.scalar_one_or_none()
        if tag:
            for contact in contacts:
                await db.refresh(contact, ["tags"])
                if tag not in contact.tags:
                    contact.tags.append(tag)

    await db.flush()
    return {"message": f"Bulk action '{data.action}' applied to {len(contacts)} contacts", "success": True}


@router.get("/{contact_id}/activities")
async def get_contact_activities(
    contact_id: str,
    current_user: User = Depends(require_perm("activities:read")),
    db: AsyncSession = Depends(get_db),
):
    from app.models.activity import Activity
    result = await db.execute(
        select(Activity).where(Activity.contact_id == contact_id).order_by(Activity.created_at.desc())
    )
    activities = result.scalars().all()
    from app.schemas.activity import ActivityResponse
    return [ActivityResponse.model_validate(a) for a in activities]


@router.get("/{contact_id}/deals")
async def get_contact_deals(
    contact_id: str,
    current_user: User = Depends(require_perm("deals:read")),
    db: AsyncSession = Depends(get_db),
):
    from app.models.deal import Deal
    result = await db.execute(
        select(Deal).where(Deal.contact_id == contact_id).order_by(Deal.created_at.desc())
    )
    deals = result.scalars().all()
    from app.schemas.deal import DealResponse
    return [DealResponse.model_validate(d) for d in deals]


@router.get("/{contact_id}/notes")
async def get_contact_notes(
    contact_id: str,
    current_user: User = Depends(require_perm("notes:read")),
    db: AsyncSession = Depends(get_db),
):
    from app.models.note import Note
    result = await db.execute(
        select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc())
    )
    notes = result.scalars().all()
    from app.schemas.note import NoteResponse
    return [NoteResponse.model_validate(n) for n in notes]
