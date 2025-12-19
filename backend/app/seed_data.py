"""
Seed script to populate database with sample data
"""
import asyncio
from app.database import get_database, connect_to_mongo, close_mongo_connection
from datetime import datetime


async def seed_data():
    """Seed database with sample projects and clients"""
    await connect_to_mongo()
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
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        # await db.projects.delete_many({})
        # await db.clients.delete_many({})
        
        # Check if data already exists
        existing_projects = await db.projects.count_documents({})
        existing_clients = await db.clients.count_documents({})
        
        if existing_projects == 0:
            result = await db.projects.insert_many(projects)
            print(f"✓ Inserted {len(result.inserted_ids)} projects")
        else:
            print(f"✓ Projects already exist ({existing_projects} projects)")
        
        if existing_clients == 0:
            result = await db.clients.insert_many(clients)
            print(f"✓ Inserted {len(result.inserted_ids)} clients")
        else:
            print(f"✓ Clients already exist ({existing_clients} clients)")
        
        print("✓ Seed data completed successfully!")
        
    except Exception as e:
        print(f"✗ Error seeding data: {e}")
        raise
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed_data())

