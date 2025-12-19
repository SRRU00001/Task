from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List
from bson import ObjectId
from app.database import get_database
from app.models.client import Client, ClientCreate, ClientUpdate
from app.utils.image_processor import crop_and_save_image
from app.auth.dependencies import get_current_admin
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/clients", tags=["clients"])
admin_router = APIRouter(prefix="/api/admin/clients", tags=["admin-clients"])


@router.get("", response_model=List[Client])
async def get_clients():
    """Get all clients"""
    try:
        db = get_database()
        clients = await db.clients.find().to_list(length=100)
        return [Client(**client) for client in clients]
    except Exception as e:
        logger.error(f"Error fetching clients: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch clients")


@admin_router.post("", response_model=Client)
async def create_client(
    name: str = Form(...),
    description: str = Form(...),
    designation: str = Form(...),
    image: UploadFile = File(...),
    current_admin: dict = Depends(get_current_admin),
):
    """Create a new client (Admin only)"""
    try:
        # Validate file extension
        file_extension = image.filename.split(".")[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Process and save image
        image_url = await crop_and_save_image(image, image.filename)
        
        # Create client document
        client_data = {
            "name": name,
            "description": description,
            "designation": designation,
            "image_url": image_url,
        }
        
        db = get_database()
        result = await db.clients.insert_one(client_data)
        client_data["_id"] = result.inserted_id
        
        return Client(**client_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create client: {str(e)}")


@router.get("/{client_id}", response_model=Client)
async def get_client(client_id: str):
    """Get a single client by ID"""
    try:
        if not ObjectId.is_valid(client_id):
            raise HTTPException(status_code=400, detail="Invalid client ID")
        
        db = get_database()
        client = await db.clients.find_one({"_id": ObjectId(client_id)})
        
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return Client(**client)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching client: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch client")


@admin_router.put("/{client_id}", response_model=Client)
async def update_client(
    client_id: str,
    name: str = Form(None),
    description: str = Form(None),
    designation: str = Form(None),
    image: UploadFile = File(None),
    current_admin: dict = Depends(get_current_admin),
):
    """Update a client (Admin only)"""
    try:
        if not ObjectId.is_valid(client_id):
            raise HTTPException(status_code=400, detail="Invalid client ID")
        
        db = get_database()
        client = await db.clients.find_one({"_id": ObjectId(client_id)})
        
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if designation is not None:
            update_data["designation"] = designation
        if image:
            # Validate file extension
            file_extension = image.filename.split(".")[-1].lower()
            if file_extension not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
                )
            # Process and save new image
            image_url = await crop_and_save_image(image, image.filename)
            update_data["image_url"] = image_url
        
        if update_data:
            await db.clients.update_one(
                {"_id": ObjectId(client_id)},
                {"$set": update_data}
            )
        
        # Fetch updated client
        updated_client = await db.clients.find_one({"_id": ObjectId(client_id)})
        return Client(**updated_client)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating client: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update client: {str(e)}")


@admin_router.delete("/{client_id}")
async def delete_client(
    client_id: str,
    current_admin: dict = Depends(get_current_admin),
):
    """Delete a client (Admin only)"""
    try:
        if not ObjectId.is_valid(client_id):
            raise HTTPException(status_code=400, detail="Invalid client ID")
        
        db = get_database()
        result = await db.clients.delete_one({"_id": ObjectId(client_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return {"message": "Client deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting client: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete client")

