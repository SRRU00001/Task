# UFM Application Architecture - Complete Technical Documentation

This document provides a comprehensive understanding of the UFM Full Stack Application architecture, explaining every component, file, function, and design decision.

---

## Table of Contents

1. [High-Level Architecture](#1-high-level-architecture)
2. [System Flow Diagram](#2-system-flow-diagram)
3. [Technology Choices & Reasoning](#3-technology-choices--reasoning)
4. [Folder Structure Explained](#4-folder-structure-explained)
5. [Backend Deep Dive](#5-backend-deep-dive)
6. [Frontend Deep Dive](#6-frontend-deep-dive)
7. [Infrastructure & Deployment](#7-infrastructure--deployment)
8. [Data Flow Examples](#8-data-flow-examples)
9. [Security Implementation](#9-security-implementation)
10. [Design Patterns Used](#10-design-patterns-used)

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    (http://localhost)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NGINX (Port 80)                             │
│              Reverse Proxy & Static File Server                  │
│  ┌─────────────────┬──────────────────┬─────────────────────┐   │
│  │ / (Frontend)    │ /api/* (Backend) │ /static/* (Uploads) │   │
│  │ Serves HTML/CSS │ Proxy to :8000   │ Proxy to :8000      │   │
│  └─────────────────┴──────────────────┴─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND (Port 8000)                    │
│  ┌───────────┬───────────┬───────────┬───────────────────────┐  │
│  │  Routers  │  Models   │   Auth    │     Utilities         │  │
│  │ (API      │ (Pydantic │ (JWT      │ (Image Processing)    │  │
│  │  Endpoints)│  Schemas)│  Tokens)  │                       │  │
│  └───────────┴───────────┴───────────┴───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONGODB ATLAS (Cloud)                         │
│  ┌───────────┬───────────┬───────────┬───────────────────────┐  │
│  │ projects  │  clients  │ contacts  │     newsletters       │  │
│  │ Collection│ Collection│ Collection│     Collection        │  │
│  └───────────┴───────────┴───────────┴───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

1. **Single Port Access (80)**: Users access everything via port 80 - simpler deployment
2. **Separation of Concerns**: Frontend, Backend, and Database are independent
3. **Scalability**: Each layer can be scaled independently
4. **Security**: Backend is not directly exposed; Nginx acts as a gateway

---

## 2. System Flow Diagram

### Request Flow for Landing Page

```
User visits http://localhost
        │
        ▼
    NGINX receives request
        │
        ▼
    Path is "/" → Serve /usr/share/nginx/html/index.html
        │
        ▼
    Browser loads index.html
        │
        ▼
    JavaScript (main.js) executes
        │
        ▼
    api.getProjects() called
        │
        ▼
    Fetch GET /api/projects
        │
        ▼
    NGINX proxies to backend:8000/api/projects
        │
        ▼
    FastAPI router handles request
        │
        ▼
    MongoDB query: db.projects.find()
        │
        ▼
    JSON response sent back
        │
        ▼
    JavaScript renders project cards
```

### Request Flow for Admin Login

```
Admin visits http://localhost/admin.html
        │
        ▼
    Enter username/password → Submit
        │
        ▼
    api.login(username, password)
        │
        ▼
    POST /api/admin/auth/login with JSON body
        │
        ▼
    FastAPI validates credentials against settings
        │
        ▼
    If valid → Generate JWT token
        │
        ▼
    Return { access_token, token_type, username }
        │
        ▼
    JavaScript stores token in localStorage
        │
        ▼
    Subsequent requests include: Authorization: Bearer <token>
```

---

## 3. Technology Choices & Reasoning

### Backend: FastAPI (Python)

**Why FastAPI?**
- **Async Support**: Built-in async/await for high performance with MongoDB
- **Automatic API Docs**: Swagger UI and ReDoc generated automatically
- **Type Hints**: Pydantic integration for request/response validation
- **Modern Python**: Clean, readable code with Python 3.11 features

### Database: MongoDB Atlas

**Why MongoDB?**
- **Schema Flexibility**: No rigid schema for evolving data models
- **JSON-Native**: Natural fit for JavaScript frontend
- **Free Tier**: MongoDB Atlas provides free cloud hosting
- **Async Driver**: Motor library for non-blocking operations

### Frontend: Vanilla HTML/CSS/JS

**Why No Framework?**
- **Simplicity**: No build step required
- **Performance**: Minimal JavaScript, fast loading
- **Portability**: Works anywhere without Node.js
- **Learning**: Clear understanding of fundamentals

### Authentication: JWT

**Why JWT?**
- **Stateless**: No server-side session storage
- **Self-Contained**: Token carries user info
- **Scalable**: Works across multiple backend instances
- **Standard**: Industry-standard authentication method

### Containerization: Docker

**Why Docker?**
- **Consistency**: Same environment everywhere
- **Isolation**: Dependencies contained
- **Easy Deployment**: Single command startup
- **Portability**: Works on any OS with Docker

---

## 4. Folder Structure Explained

```
UFM/
├── backend/                    # Python FastAPI application
│   ├── app/                    # Main application package
│   │   ├── __init__.py         # Makes 'app' a Python package
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── config.py           # Environment configuration
│   │   ├── database.py         # MongoDB connection management
│   │   ├── seed_data.py        # Sample data generator
│   │   │
│   │   ├── models/             # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── project.py      # Project schema
│   │   │   ├── client.py       # Client schema
│   │   │   ├── contact.py      # Contact form schema
│   │   │   └── newsletter.py   # Newsletter schema
│   │   │
│   │   ├── routers/            # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── projects.py     # Project CRUD endpoints
│   │   │   ├── clients.py      # Client CRUD endpoints
│   │   │   ├── contact.py      # Contact form endpoints
│   │   │   ├── newsletter.py   # Newsletter endpoints
│   │   │   ├── admin.py        # Authentication endpoints
│   │   │   └── seed.py         # Database seeding endpoints
│   │   │
│   │   ├── auth/               # Authentication logic
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py          # JWT token creation/verification
│   │   │   └── dependencies.py # FastAPI dependencies for auth
│   │   │
│   │   ├── utils/              # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── image_processor.py  # Image cropping/resizing
│   │   │
│   │   └── static/             # Static files served by FastAPI
│   │       └── uploads/        # Uploaded images storage
│   │
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Container build instructions
│
├── frontend/                   # Static web frontend
│   ├── index.html              # Landing page
│   ├── admin.html              # Admin panel
│   ├── css/
│   │   ├── style.css           # Landing page styles
│   │   └── admin.css           # Admin panel styles
│   ├── js/
│   │   ├── api.js              # API client class
│   │   ├── main.js             # Landing page logic
│   │   └── admin.js            # Admin panel logic
│   └── images/                 # Frontend static images
│
├── nginx/
│   └── nginx.conf              # Reverse proxy configuration
│
├── docker-compose.yml          # Multi-container orchestration
├── .env                        # Environment variables (gitignored)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # Setup instructions
└── Understand.md               # This architecture document
```

### Why This Structure?

1. **`backend/app/`**: Encapsulates all Python code as a package for clean imports
2. **`models/`**: Separate data schemas for maintainability
3. **`routers/`**: Each domain (projects, clients) has its own router file
4. **`auth/`**: Centralized authentication logic
5. **`utils/`**: Reusable utility functions
6. **`frontend/`**: Completely separate from backend (can be deployed independently)
7. **`nginx/`**: Infrastructure configuration isolated

---

## 5. Backend Deep Dive

### 5.1 `backend/app/main.py` - Application Entry Point

**Purpose**: Initialize FastAPI app, configure middleware, include routers

```python
# Key Components:

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events
    - Startup: Connect to MongoDB, create uploads directory
    - Shutdown: Close MongoDB connection
    """

app = FastAPI(
    title="UFM Full Stack Application",
    lifespan=lifespan  # Modern way to handle lifecycle
)

def custom_openapi():
    """
    Customize OpenAPI schema to add Bearer auth to Swagger UI
    Allows testing protected endpoints in /docs
    """

# CORS Middleware - Allows frontend to call API
app.add_middleware(CORSMiddleware, ...)

# Include all routers
app.include_router(projects.router)        # Public project routes
app.include_router(projects.admin_router)  # Protected project routes
# ... more routers

# Static file mounting for uploaded images
app.mount("/static", StaticFiles(directory=static_dir))
```

**Why Lifespan Context Manager?**
- Modern FastAPI approach (replaces deprecated `@app.on_event`)
- Ensures proper cleanup on shutdown
- Async-aware for database connections

---

### 5.2 `backend/app/config.py` - Configuration Management

**Purpose**: Centralize all configuration with environment variable support

```python
class Settings(BaseSettings):
    """
    Pydantic-based settings management
    Automatically reads from environment variables and .env file
    """
    
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/ufm_db")
    DATABASE_NAME: str = "ufm_db"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "...")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Admin Credentials
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # CORS - Which origins can call our API
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Image Processing
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "static/uploads")
    IMAGE_CROP_WIDTH: int = 450
    IMAGE_CROP_HEIGHT: int = 350

settings = Settings()  # Singleton instance
```

**Why Pydantic Settings?**
- Type validation for configuration values
- Automatic environment variable loading
- Default values with override capability
- Single source of truth for configuration

---

### 5.3 `backend/app/database.py` - Database Connection

**Purpose**: Manage MongoDB connection lifecycle

```python
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    """Holds the MongoDB client instance"""
    client: AsyncIOMotorClient = None

db = Database()  # Global database holder

async def connect_to_mongo():
    """
    Called on application startup
    Creates async MongoDB client and tests connection
    """
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    await db.client.admin.command('ping')  # Verify connection
    logger.info("Connected to MongoDB successfully")

async def close_mongo_connection():
    """Called on application shutdown"""
    if db.client:
        db.client.close()

def get_database():
    """
    Returns the database instance for the configured database name
    Used by routers to perform database operations
    """
    return db.client[settings.DATABASE_NAME]
```

**Why Motor?**
- Official async MongoDB driver for Python
- Non-blocking I/O operations
- Perfect fit for FastAPI's async nature

---

### 5.4 `backend/app/models/` - Pydantic Data Models

#### `project.py` - Project Schema

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from bson import ObjectId

class Project(BaseModel):
    """
    Represents a project document from MongoDB
    Used for API responses
    """
    model_config = ConfigDict(
        populate_by_name=True,      # Accept both 'id' and '_id'
        json_encoders={ObjectId: str}  # Serialize ObjectId to string
    )
    
    id: Optional[str] = Field(default=None, validation_alias="_id")
    image_url: str
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        """Convert MongoDB ObjectId to string"""
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None


class ProjectCreate(BaseModel):
    """Schema for creating a project (no id, no image_url)"""
    name: str
    description: str


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
```

**Why Three Classes?**
1. **Project**: Full model for responses (includes id, image_url, timestamps)
2. **ProjectCreate**: What client sends when creating (no id yet, image sent separately)
3. **ProjectUpdate**: Partial update support (only changed fields)

**Why `validation_alias="_id"`?**
- MongoDB uses `_id` as the primary key
- API returns `id` for cleaner JSON
- Pydantic handles the mapping automatically

---

### 5.5 `backend/app/routers/` - API Endpoints

#### `projects.py` - Project CRUD Operations

```python
# Two routers: public and admin
router = APIRouter(prefix="/api/projects", tags=["projects"])
admin_router = APIRouter(prefix="/api/admin/projects", tags=["admin-projects"])

@router.get("", response_model=List[Project])
async def get_projects():
    """
    GET /api/projects
    Public endpoint - no auth required
    Returns all projects from database
    """
    db = get_database()
    projects = await db.projects.find().to_list(length=100)
    return [Project(**project) for project in projects]


@admin_router.post("", response_model=Project)
async def create_project(
    name: str = Form(...),           # Form field (multipart)
    description: str = Form(...),    # Form field (multipart)
    image: UploadFile = File(...),   # File upload
    current_admin: dict = Depends(get_current_admin),  # Auth dependency
):
    """
    POST /api/admin/projects
    Protected endpoint - requires JWT token
    Creates project with image upload and auto-crop
    """
    # Validate file extension
    file_extension = image.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Process image (crop to 450x350)
    image_url = await crop_and_save_image(image, image.filename)
    
    # Insert into database
    project_data = {"name": name, "description": description, "image_url": image_url}
    result = await db.projects.insert_one(project_data)
    project_data["_id"] = result.inserted_id
    
    return Project(**project_data)
```

**Why Two Routers?**
- `router`: Public endpoints (GET operations)
- `admin_router`: Protected endpoints (POST, PUT, DELETE)
- Clear separation of public vs protected routes
- Different URL prefixes (`/api/projects` vs `/api/admin/projects`)

**Why Form() and File()?**
- Image upload requires `multipart/form-data`
- Can't use JSON body with file uploads
- Form() extracts text fields from multipart request
- File() extracts uploaded file

---

### 5.6 `backend/app/auth/` - Authentication

#### `jwt.py` - Token Management

```python
from jose import jwt, JWTError

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token with the given data and expiration
    
    Args:
        data: Payload to encode (e.g., {"sub": "admin", "username": "admin"})
        expires_delta: How long until token expires
    
    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token
    
    Returns:
        Decoded payload if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

#### `dependencies.py` - FastAPI Dependencies

```python
def get_current_admin(request: Request) -> dict:
    """
    FastAPI dependency for protecting endpoints
    
    Usage: current_admin: dict = Depends(get_current_admin)
    
    1. Extracts Authorization header
    2. Validates Bearer token format
    3. Verifies JWT token
    4. Returns decoded payload or raises 401
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload
```

**Why Dependencies?**
- Reusable authentication logic
- Declarative security (add `Depends()` to any endpoint)
- Automatic 401 response for unauthorized requests
- Clean separation of auth logic from business logic

---

### 5.7 `backend/app/utils/image_processor.py` - Image Processing

```python
from PIL import Image
import uuid

async def crop_and_save_image(image_file, filename: str) -> str:
    """
    Process uploaded image: crop to 450x350 and save
    
    Algorithm:
    1. Read image bytes from upload
    2. Calculate crop dimensions to maintain aspect ratio
    3. Center-crop to target ratio
    4. Resize to exact 450x350
    5. Save with unique filename
    6. Return URL path
    
    Args:
        image_file: FastAPI UploadFile object
        filename: Original filename (for extension)
    
    Returns:
        URL path like "/static/uploads/uuid.png"
    """
    # Read image
    image_bytes = await image_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # Calculate crop dimensions
    original_width, original_height = image.size
    target_ratio = 450 / 350  # ~1.286
    
    if original_width / original_height > target_ratio:
        # Image is wider - crop sides
        new_height = original_height
        new_width = int(original_height * target_ratio)
        left = (original_width - new_width) // 2  # Center
        top = 0
    else:
        # Image is taller - crop top/bottom
        new_width = original_width
        new_height = int(original_width / target_ratio)
        left = 0
        top = (original_height - new_height) // 2  # Center
    
    # Crop and resize
    cropped = image.crop((left, top, left + new_width, top + new_height))
    resized = cropped.resize((450, 350), Image.Resampling.LANCZOS)
    
    # Generate unique filename and save
    unique_filename = f"{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    file_path = os.path.join(upload_dir, unique_filename)
    resized.save(file_path, quality=85, optimize=True)
    
    return f"/static/uploads/{unique_filename}"
```

**Why This Algorithm?**
1. **Center Crop**: Keeps the most important part (usually center)
2. **Aspect Ratio First**: Prevents distortion
3. **LANCZOS Resampling**: High-quality downscaling
4. **UUID Filenames**: Prevents naming conflicts
5. **Quality 85%**: Good balance of size vs quality

---

## 6. Frontend Deep Dive

### 6.1 `frontend/js/api.js` - API Client

**Purpose**: Centralized HTTP communication with backend

```javascript
class API {
    constructor() {
        // Load token from localStorage on initialization
        this.token = localStorage.getItem('admin_token');
    }
    
    setToken(token) {
        /**
         * Store or clear JWT token
         * Persists to localStorage for page refreshes
         */
        this.token = token;
        if (token) {
            localStorage.setItem('admin_token', token);
        } else {
            localStorage.removeItem('admin_token');
        }
    }
    
    getAuthHeader() {
        /**
         * Build Authorization header for protected requests
         * Returns empty object if no token
         */
        if (this.token) {
            return { 'Authorization': `Bearer ${this.token}` };
        }
        return {};
    }
    
    async request(endpoint, options = {}) {
        /**
         * Generic request method
         * Handles:
         * - URL construction
         * - Content-Type headers (JSON vs FormData)
         * - Auth header injection
         * - Error handling
         */
        const url = `${API_BASE_URL}${endpoint}`;
        const isFormData = options.body instanceof FormData;
        
        const headers = {};
        
        // Don't set Content-Type for FormData (browser sets it with boundary)
        if (!isFormData && options.method && options.method !== 'GET') {
            headers['Content-Type'] = 'application/json';
        }
        
        // Add auth header if required
        if (options.requireAuth) {
            Object.assign(headers, this.getAuthHeader());
        }
        
        const response = await fetch(url, {
            method: options.method || 'GET',
            headers,
            body: options.body
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        
        return data;
    }
    
    // Public endpoints (no auth)
    async getProjects() {
        return this.request('/projects');
    }
    
    async getClients() {
        return this.request('/clients');
    }
    
    // Admin endpoints (with auth)
    async createProject(formData) {
        /**
         * Special handling for file upload
         * Uses direct fetch instead of request() method
         * because FormData needs special header handling
         */
        const response = await fetch(`${API_BASE_URL}/admin/projects`, {
            method: 'POST',
            headers: this.getAuthHeader(),  // Only auth header, no Content-Type
            body: formData,  // FormData object with file
        });
        // ...
    }
}

const api = new API();  // Global singleton
```

**Why a Class?**
- Encapsulates token state
- Reusable request method
- Clean API for different endpoints
- Easy to extend with new methods

---

### 6.2 `frontend/js/main.js` - Landing Page Logic

```javascript
// Placeholder image for failed loads
const PLACEHOLDER_IMAGE = "data:image/svg+xml,...";

document.addEventListener('DOMContentLoaded', async () => {
    /**
     * Entry point - runs when HTML is fully loaded
     * Loads data and sets up event listeners
     */
    await loadProjects();
    await loadClients();
    setupContactForm();
    setupNewsletterForm();
});

async function loadProjects() {
    /**
     * Fetch projects from API and render cards
     */
    const projects = await api.getProjects();
    const container = document.getElementById('projects-container');
    
    container.innerHTML = projects.map(project => `
        <div class="project-card">
            <img src="${project.image_url}" 
                 onerror="this.src='${PLACEHOLDER_IMAGE}'">
            <h3>${escapeHtml(project.name)}</h3>
            <p>${escapeHtml(project.description)}</p>
        </div>
    `).join('');
}

function setupContactForm() {
    /**
     * Handle contact form submission
     * Validates input, shows feedback, resets form
     */
    const form = document.getElementById('contact-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            full_name: document.getElementById('full-name').value,
            email: document.getElementById('email').value,
            mobile_number: document.getElementById('mobile-number').value,
            city: document.getElementById('city').value,
        };
        
        // Validation
        if (!isValidEmail(formData.email)) {
            showMessage('Invalid email', 'error');
            return;
        }
        
        await api.submitContact(formData);
        showMessage('Submitted successfully!', 'success');
        form.reset();
    });
}

function escapeHtml(text) {
    /**
     * Prevent XSS attacks by escaping HTML characters
     * Converts <script> to &lt;script&gt;
     */
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

---

### 6.3 `frontend/js/admin.js` - Admin Panel Logic

```javascript
let currentEditingProject = null;  // Tracks edit state

document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();      // Verify token on load
    setupAuth();            // Setup login/logout handlers
    setupProjectManagement();
    setupClientManagement();
});

async function checkAuth() {
    /**
     * Verify if user is authenticated
     * Shows login screen or admin panel accordingly
     */
    try {
        await api.verifyAdmin();  // Throws if token invalid
        showAdminPanel();
    } catch {
        showLoginScreen();
    }
}

function setupAuth() {
    /**
     * Handle login form submission
     */
    const loginForm = document.getElementById('login-form');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        const response = await api.login(username, password);
        api.setToken(response.access_token);  // Store token
        await checkAuth();  // Refresh view
    });
}

async function handleProjectSubmit(e) {
    /**
     * Handle project create/update
     * Uses FormData for file upload
     */
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('project-name').value);
    formData.append('description', document.getElementById('project-description').value);
    
    const imageFile = document.getElementById('project-image').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
    }
    
    if (currentEditingProject) {
        await api.updateProject(currentEditingProject.id, formData);
    } else {
        await api.createProject(formData);
    }
    
    await loadProjectsAdmin();  // Refresh list
}

// Make functions available globally for onclick handlers
window.editProject = editProject;
window.deleteProject = deleteProject;
```

---

## 7. Infrastructure & Deployment

### 7.1 `docker-compose.yml` - Container Orchestration

```yaml
services:
  backend:
    build:
      context: ./backend     # Build from backend folder
      dockerfile: Dockerfile
    container_name: ufm_backend
    environment:
      # Pass environment variables from .env file
      - MONGODB_URI=${MONGODB_URI}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ADMIN_USERNAME=${ADMIN_USERNAME:-admin}  # Default if not set
    volumes:
      # Persist uploaded images on host
      - ./backend/app/static/uploads:/app/app/static/uploads
    ports:
      - "8000:8000"  # Expose for debugging (optional)
    networks:
      - ufm_network
  
  nginx:
    image: nginx:alpine     # Pre-built image
    container_name: ufm_nginx
    ports:
      - "80:80"             # Main entry point
    volumes:
      - ./frontend:/usr/share/nginx/html:ro   # Frontend files
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro  # Config
    depends_on:
      - backend             # Start backend first
    networks:
      - ufm_network

networks:
  ufm_network:
    driver: bridge          # Internal network for container communication
```

**Why Docker Compose?**
- Define multi-container application
- Single command to start everything
- Network isolation between containers
- Easy environment variable management

---

### 7.2 `nginx/nginx.conf` - Reverse Proxy

```nginx
upstream backend {
    server backend:8000;  # Docker DNS resolves 'backend' to container
}

server {
    listen 80;
    
    # Frontend - Serve static HTML/CSS/JS
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;  # SPA fallback
    }
    
    # API - Proxy to FastAPI backend
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 10M;  # For file uploads
    }
    
    # Static uploads - Proxy to backend's /static
    location ^~ /static {
        proxy_pass http://backend;
        # ^~ gives priority over regex patterns
    }
    
    # Swagger docs - Proxy to backend
    location /docs {
        proxy_pass http://backend/docs;
    }
}
```

**Why Nginx?**
- High-performance static file serving
- Reverse proxy capabilities
- Single port for entire application
- Caching and compression built-in

---

### 7.3 `backend/Dockerfile` - Backend Container

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install gcc for packages that need compilation
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p app/static/uploads

EXPOSE 8000

# Run with uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why Slim Image?**
- Smaller image size (~150MB vs ~1GB full)
- Faster builds and deployments
- Security (fewer packages = smaller attack surface)

---

## 8. Data Flow Examples

### Example 1: Creating a Project

```
1. Admin fills form in admin.html
   ├── Name: "New Project"
   ├── Description: "Project description"
   └── Image: photo.jpg (2MB)

2. JavaScript (admin.js)
   ├── Create FormData object
   ├── Append form fields
   ├── Append image file
   └── Call api.createProject(formData)

3. api.js createProject()
   ├── Build request with auth header
   ├── POST to /api/admin/projects
   └── Body: FormData (multipart/form-data)

4. Nginx
   ├── Matches /api prefix
   └── Proxies to backend:8000

5. FastAPI (projects.py admin_router)
   ├── Depends(get_current_admin) verifies JWT
   ├── Extracts Form fields (name, description)
   ├── Extracts File (image)
   └── Calls crop_and_save_image()

6. image_processor.py
   ├── Reads image bytes
   ├── Crops to 450x350
   ├── Generates UUID filename
   ├── Saves to /app/app/static/uploads/
   └── Returns "/static/uploads/uuid.png"

7. FastAPI continues
   ├── Inserts document to MongoDB
   └── Returns Project JSON

8. JavaScript receives response
   ├── Refreshes project list
   └── Shows success message
```

### Example 2: Viewing Projects (Public)

```
1. User visits http://localhost
   └── Nginx serves index.html

2. Browser loads main.js
   └── Calls loadProjects()

3. api.getProjects()
   └── Fetch GET /api/projects

4. Nginx proxies to backend

5. FastAPI (projects.py router)
   ├── No auth required (public endpoint)
   ├── Query: db.projects.find()
   └── Returns list of Project JSON

6. JavaScript
   ├── Maps projects to HTML cards
   └── Injects into #projects-container

7. Browser renders cards
   ├── Images load from /static/uploads/
   └── Nginx proxies to backend static files
```

---

## 9. Security Implementation

### 9.1 Authentication Flow

```
┌─────────────┐     POST /api/admin/auth/login     ┌─────────────┐
│   Browser   │ ──────────────────────────────────▶│   Backend   │
│             │     { username, password }          │             │
└─────────────┘                                     └─────────────┘
                                                           │
                                                           ▼
                                                    Validate credentials
                                                    against settings
                                                           │
                                                           ▼
┌─────────────┐      { access_token, ... }          ┌─────────────┐
│   Browser   │ ◀──────────────────────────────────│   Backend   │
│             │                                     │             │
└─────────────┘                                     └─────────────┘
       │
       ▼
Store token in localStorage
       │
       ▼
Future requests include:
Authorization: Bearer <token>
```

### 9.2 Security Measures

| Measure | Implementation | Purpose |
|---------|----------------|---------|
| JWT Tokens | `python-jose` library | Stateless authentication |
| Token Expiration | 24 hours | Limit token lifetime |
| Password Hashing | Environment variable | Keep credentials secure |
| CORS | FastAPI middleware | Prevent unauthorized origins |
| Input Validation | Pydantic models | Reject malformed data |
| XSS Prevention | `escapeHtml()` in JS | Sanitize displayed content |
| File Validation | Extension whitelist | Prevent malicious uploads |
| SQL Injection | N/A (MongoDB) | NoSQL doesn't use SQL |

---

## 10. Design Patterns Used

### 10.1 Repository Pattern (Implicit)

```python
# Routers act as pseudo-repositories
# All database access goes through get_database()

async def get_projects():
    db = get_database()
    return await db.projects.find().to_list(100)
```

### 10.2 Dependency Injection

```python
# FastAPI's Depends() for reusable logic

@admin_router.post("")
async def create_project(
    current_admin: dict = Depends(get_current_admin),  # Injected
):
    # current_admin is automatically validated
    pass
```

### 10.3 Singleton Pattern

```python
# Single settings instance
settings = Settings()

# Single database holder
db = Database()

# Single API client
const api = new API();
```

### 10.4 Factory Pattern

```python
# Pydantic models act as factories
project = Project(**raw_dict)  # Creates validated object
```

### 10.5 Adapter Pattern

```python
# ObjectId to string conversion
@field_validator('id', mode='before')
def validate_id(cls, v):
    if isinstance(v, ObjectId):
        return str(v)  # Adapt MongoDB ObjectId to JSON string
    return v
```

---

## Summary

This architecture follows modern best practices:

1. **Separation of Concerns**: Frontend, Backend, Database are independent
2. **Single Responsibility**: Each file/class has one purpose
3. **DRY (Don't Repeat Yourself)**: Reusable components (models, dependencies)
4. **Security First**: JWT auth, input validation, CORS
5. **Developer Experience**: Auto-generated API docs, clear folder structure
6. **Deployment Ready**: Docker containers, environment variables

The result is a maintainable, scalable, and secure full-stack application.

