from fastapi import APIRouter
from app.api.v1 import auth, users, contacts, companies, deals, activities, notes, tags, email_templates, notifications, webhooks, reports, search, dashboard

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(contacts.router)
router.include_router(companies.router)
router.include_router(deals.router)
router.include_router(activities.router)
router.include_router(notes.router)
router.include_router(tags.router)
router.include_router(email_templates.router)
router.include_router(notifications.router)
router.include_router(webhooks.router)
router.include_router(reports.router)
router.include_router(search.router)
router.include_router(dashboard.router)
