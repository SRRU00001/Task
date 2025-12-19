from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.database import get_database
from app.models.newsletter import Newsletter, NewsletterCreate
from app.auth.dependencies import get_current_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])
admin_router = APIRouter(prefix="/api/admin/newsletters", tags=["admin-newsletters"])


@router.post("", response_model=Newsletter)
async def subscribe_newsletter(newsletter: NewsletterCreate):
    """Subscribe to newsletter"""
    try:
        db = get_database()
        
        # Check if email already exists
        existing = await db.newsletters.find_one({"email": newsletter.email})
        if existing:
            return Newsletter(**existing)
        
        newsletter_data = newsletter.dict()
        result = await db.newsletters.insert_one(newsletter_data)
        newsletter_data["_id"] = result.inserted_id
        return Newsletter(**newsletter_data)
    except Exception as e:
        logger.error(f"Error subscribing to newsletter: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to subscribe: {str(e)}")


@admin_router.get("", response_model=List[Newsletter])
async def get_newsletters(current_admin: dict = Depends(get_current_admin)):
    """Get all newsletter subscriptions (Admin only)"""
    try:
        db = get_database()
        newsletters = await db.newsletters.find().sort("subscribed_at", -1).to_list(length=1000)
        return [Newsletter(**newsletter) for newsletter in newsletters]
    except Exception as e:
        logger.error(f"Error fetching newsletters: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch newsletters")

