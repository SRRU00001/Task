from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.database import get_database
from app.models.contact import Contact, ContactCreate
from app.auth.dependencies import get_current_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contact", tags=["contact"])
admin_router = APIRouter(prefix="/api/admin/contacts", tags=["admin-contacts"])


@router.post("", response_model=Contact)
async def create_contact(contact: ContactCreate):
    """Submit contact form"""
    try:
        db = get_database()
        contact_data = contact.dict()
        result = await db.contacts.insert_one(contact_data)
        contact_data["_id"] = result.inserted_id
        return Contact(**contact_data)
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit contact form: {str(e)}")


@admin_router.get("", response_model=List[Contact])
async def get_contacts(current_admin: dict = Depends(get_current_admin)):
    """Get all contact form submissions (Admin only)"""
    try:
        db = get_database()
        contacts = await db.contacts.find().sort("created_at", -1).to_list(length=1000)
        return [Contact(**contact) for contact in contacts]
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch contacts")

