from fastapi import HTTPException, Request
from app.auth.jwt import verify_token
import logging

logger = logging.getLogger(__name__)


def get_current_admin(request: Request) -> dict:
    """Dependency to verify admin JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload

