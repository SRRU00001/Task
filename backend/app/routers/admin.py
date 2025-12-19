from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_admin
from app.config import settings
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/auth/login")
async def admin_login(login_data: LoginRequest):
    """Admin login with username and password"""
    try:
        # Verify credentials
        if login_data.username != settings.ADMIN_USERNAME or login_data.password != settings.ADMIN_PASSWORD:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Create JWT token
        jwt_token = create_access_token(
            data={
                "sub": login_data.username,
                "username": login_data.username,
            },
            expires_delta=timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        )
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "username": login_data.username
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in admin login: {e}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/auth/verify")
async def verify_admin(current_admin: dict = Depends(get_current_admin)):
    """Verify admin token"""
    return {
        "authenticated": True,
        "user": {
            "username": current_admin.get("sub"),
        }
    }


@router.get("/auth/logout")
async def logout():
    """Logout endpoint (client-side token removal)"""
    return {"message": "Logged out successfully"}

