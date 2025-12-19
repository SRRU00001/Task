from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging
import os

from app.database import connect_to_mongo, close_mongo_connection
from app.config import settings
from app.routers import projects, clients, contact, newsletter, admin, seed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    # Create uploads directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="UFM Full Stack Application",
    description="Full stack application with FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan
)


# Custom OpenAPI schema with security
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="UFM Full Stack Application",
        version="1.0.0",
        description="Full stack application with FastAPI and MongoDB. Use /api/admin/auth/login to get a token.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token from /api/admin/auth/login"
        }
    }
    # Apply security to all admin routes
    for path in openapi_schema["paths"]:
        if "/admin/" in path and path != "/api/admin/auth/login":
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(projects.admin_router)
app.include_router(clients.router)
app.include_router(clients.admin_router)
app.include_router(contact.router)
app.include_router(contact.admin_router)
app.include_router(newsletter.router)
app.include_router(newsletter.admin_router)
app.include_router(admin.router)
app.include_router(seed.router)

# Mount static files for uploaded images
static_dir = os.path.join(os.path.dirname(__file__), "static")
uploads_dir = os.path.join(static_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "UFM API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

