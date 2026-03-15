from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from app.api.deps import get_current_user, require_perm

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("", response_model=NoteListResponse)
async def list_notes(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    contact_id: str = Query(None),
    deal_id: str = Query(None),
    company_id: str = Query(None),
    current_user: User = Depends(require_perm("notes:read")),
    db: AsyncSession = Depends(get_db),
):
    query = select(Note)
    count_query = select(func.count(Note.id))

    if current_user.organization_id:
        query = query.where(Note.organization_id == current_user.organization_id)
        count_query = count_query.where(Note.organization_id == current_user.organization_id)

    if contact_id:
        query = query.where(Note.contact_id == contact_id)
        count_query = count_query.where(Note.contact_id == contact_id)
    if deal_id:
        query = query.where(Note.deal_id == deal_id)
        count_query = count_query.where(Note.deal_id == deal_id)
    if company_id:
        query = query.where(Note.company_id == company_id)
        count_query = count_query.where(Note.company_id == company_id)

    total = await db.scalar(count_query) or 0
    offset = (page - 1) * per_page
    result = await db.execute(query.order_by(Note.created_at.desc()).offset(offset).limit(per_page))
    notes = result.scalars().all()

    return NoteListResponse(
        items=[NoteResponse.model_validate(n) for n in notes],
        total=total, page=page, per_page=per_page,
        pages=(total + per_page - 1) // per_page if per_page else 0,
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    current_user: User = Depends(require_perm("notes:read")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse.model_validate(note)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    data: NoteCreate,
    current_user: User = Depends(require_perm("notes:write")),
    db: AsyncSession = Depends(get_db),
):
    note = Note(
        **data.model_dump(),
        user_id=current_user.id,
        organization_id=current_user.organization_id,
    )
    db.add(note)
    await db.flush()
    await db.refresh(note)
    return NoteResponse.model_validate(note)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    data: NoteUpdate,
    current_user: User = Depends(require_perm("notes:write")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(note, key, value)
    await db.flush()
    await db.refresh(note)
    return NoteResponse.model_validate(note)


@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    current_user: User = Depends(require_perm("notes:delete")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(note)
    await db.flush()
    return {"message": "Note deleted", "success": True}
