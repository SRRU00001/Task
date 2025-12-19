from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request
from typing import List
from bson import ObjectId
from app.database import get_database
from app.models.project import Project, ProjectCreate, ProjectUpdate
from app.utils.image_processor import crop_and_save_image
from app.auth.dependencies import get_current_admin
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projects", tags=["projects"])
admin_router = APIRouter(prefix="/api/admin/projects", tags=["admin-projects"])


@router.get("", response_model=List[Project])
async def get_projects():
    """Get all projects"""
    try:
        db = get_database()
        projects = await db.projects.find().to_list(length=100)
        return [Project(**project) for project in projects]
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch projects")


@admin_router.post("", response_model=Project)
async def create_project(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    current_admin: dict = Depends(get_current_admin),
):
    """Create a new project (Admin only)"""
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
        
        # Create project document
        project_data = {
            "name": name,
            "description": description,
            "image_url": image_url,
        }
        
        db = get_database()
        result = await db.projects.insert_one(project_data)
        project_data["_id"] = result.inserted_id
        
        return Project(**project_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Get a single project by ID"""
    try:
        if not ObjectId.is_valid(project_id):
            raise HTTPException(status_code=400, detail="Invalid project ID")
        
        db = get_database()
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return Project(**project)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching project: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch project")


@admin_router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    name: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
    current_admin: dict = Depends(get_current_admin),
):
    """Update a project (Admin only)"""
    try:
        if not ObjectId.is_valid(project_id):
            raise HTTPException(status_code=400, detail="Invalid project ID")
        
        db = get_database()
        project = await db.projects.find_one({"_id": ObjectId(project_id)})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
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
            await db.projects.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": update_data}
            )
        
        # Fetch updated project
        updated_project = await db.projects.find_one({"_id": ObjectId(project_id)})
        return Project(**updated_project)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")


@admin_router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_admin: dict = Depends(get_current_admin),
):
    """Delete a project (Admin only)"""
    try:
        if not ObjectId.is_valid(project_id):
            raise HTTPException(status_code=400, detail="Invalid project ID")
        
        db = get_database()
        result = await db.projects.delete_one({"_id": ObjectId(project_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete project")

