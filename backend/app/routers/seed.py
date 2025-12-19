"""
Seed endpoint for populating database
"""
from fastapi import APIRouter, HTTPException
from app.database import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/seed", tags=["seed"])


@router.post("/populate")
async def populate_seed_data():
    """Populate database with sample data"""
    try:
        db = get_database()
        
        # Sample projects
        projects = [
            {
                "name": "Consultation Project",
                "description": "Strategic business consultation services for enterprise clients. We provide expert guidance to help your business grow and succeed.",
                "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Design Project",
                "description": "Creative design solutions that transform your brand identity. Our design team creates stunning visuals that captivate your audience.",
                "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Marketing & Design",
                "description": "Comprehensive marketing strategies combined with exceptional design. We help you reach your target audience effectively.",
                "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Consultation & Marketing",
                "description": "End-to-end business solutions combining strategic consultation with powerful marketing campaigns.",
                "image_url": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Digital Transformation",
                "description": "Modernize your business with cutting-edge digital solutions. We help you stay ahead in the digital age.",
                "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            }
        ]
        
        # Sample clients
        clients = [
            {
                "name": "John Smith",
                "description": "UFM has transformed our business operations. Their expertise and dedication are unmatched. Highly recommended!",
                "designation": "CEO, Tech Solutions Inc.",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Sarah Johnson",
                "description": "Working with UFM was a game-changer. They delivered exceptional results and exceeded our expectations.",
                "designation": "Marketing Director, Global Brands",
                "image_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Michael Chen",
                "description": "Professional, reliable, and results-driven. UFM helped us achieve our goals faster than we imagined.",
                "designation": "Web Developer, Digital Innovations",
                "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Emily Davis",
                "description": "The team at UFM is incredibly talented. They understand our vision and bring it to life beautifully.",
                "designation": "Designer, Creative Studio",
                "image_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "David Wilson",
                "description": "Outstanding service and attention to detail. UFM is our go-to partner for all business needs.",
                "designation": "Operations Manager, Enterprise Corp",
                "image_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            }
        ]
        
        # Check if data already exists
        existing_projects = await db.projects.count_documents({})
        existing_clients = await db.clients.count_documents({})
        
        projects_inserted = 0
        clients_inserted = 0
        
        if existing_projects == 0:
            result = await db.projects.insert_many(projects)
            projects_inserted = len(result.inserted_ids)
        
        if existing_clients == 0:
            result = await db.clients.insert_many(clients)
            clients_inserted = len(result.inserted_ids)
        
        return {
            "message": "Seed data populated successfully",
            "projects_inserted": projects_inserted,
            "clients_inserted": clients_inserted,
            "existing_projects": existing_projects,
            "existing_clients": existing_clients
        }
        
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed data: {str(e)}")


@router.post("/reset")
async def reset_and_reseed():
    """Clear all data and reseed with sample data"""
    try:
        db = get_database()
        
        # Delete all projects and clients
        deleted_projects = await db.projects.delete_many({})
        deleted_clients = await db.clients.delete_many({})
        
        # Now populate with seed data
        projects = [
            {
                "name": "Consultation Project",
                "description": "Strategic business consultation services for enterprise clients. We provide expert guidance to help your business grow and succeed.",
                "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Design Project",
                "description": "Creative design solutions that transform your brand identity. Our design team creates stunning visuals that captivate your audience.",
                "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Marketing & Design",
                "description": "Comprehensive marketing strategies combined with exceptional design. We help you reach your target audience effectively.",
                "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Consultation & Marketing",
                "description": "End-to-end business solutions combining strategic consultation with powerful marketing campaigns.",
                "image_url": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Digital Transformation",
                "description": "Modernize your business with cutting-edge digital solutions. We help you stay ahead in the digital age.",
                "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            }
        ]
        
        clients = [
            {
                "name": "John Smith",
                "description": "UFM has transformed our business operations. Their expertise and dedication are unmatched. Highly recommended!",
                "designation": "CEO, Tech Solutions Inc.",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Sarah Johnson",
                "description": "Working with UFM was a game-changer. They delivered exceptional results and exceeded our expectations.",
                "designation": "Marketing Director, Global Brands",
                "image_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Michael Chen",
                "description": "Professional, reliable, and results-driven. UFM helped us achieve our goals faster than we imagined.",
                "designation": "Web Developer, Digital Innovations",
                "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "Emily Davis",
                "description": "The team at UFM is incredibly talented. They understand our vision and bring it to life beautifully.",
                "designation": "Designer, Creative Studio",
                "image_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            },
            {
                "name": "David Wilson",
                "description": "Outstanding service and attention to detail. UFM is our go-to partner for all business needs.",
                "designation": "Operations Manager, Enterprise Corp",
                "image_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=450&h=350&fit=crop",
                "created_at": datetime.utcnow()
            }
        ]
        
        await db.projects.insert_many(projects)
        await db.clients.insert_many(clients)
        
        return {
            "message": "Database reset and reseeded successfully",
            "deleted_projects": deleted_projects.deleted_count,
            "deleted_clients": deleted_clients.deleted_count,
            "new_projects": len(projects),
            "new_clients": len(clients)
        }
        
    except Exception as e:
        logger.error(f"Error resetting data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset data: {str(e)}")

