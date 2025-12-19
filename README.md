# UFM Full Stack Application

A full-stack web application built with FastAPI backend, MongoDB database, and vanilla HTML/CSS/JS frontend. Features project management, client testimonials, contact form, newsletter subscription, and an admin panel.

---

## 🚀 Quick Start (5 Minutes Setup)

### Prerequisites

Before you begin, ensure you have installed:
- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download here](https://git-scm.com/downloads)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd UFM
```

### Step 2: Create Environment File

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

### Step 3: Start the Application

**Windows (PowerShell):**
```powershell
docker-compose up --build -d
```

**Mac/Linux:**
```bash
docker-compose up --build -d
```

### Step 4: Populate Sample Data

**Windows (PowerShell):**
```powershell
Start-Sleep -Seconds 10; Invoke-WebRequest -Uri "http://localhost/api/seed/populate" -Method POST -UseBasicParsing
```

**Mac/Linux:**
```bash
sleep 10 && curl -X POST http://localhost/api/seed/populate
```

### Step 5: Access the Application

| Page | URL |
|------|-----|
| **Landing Page** | http://localhost |
| **Admin Panel** | http://localhost/admin.html |
| **API Documentation (Swagger)** | http://localhost/docs |
| **API Documentation (ReDoc)** | http://localhost/redoc |

### Admin Login Credentials

- **Username:** `admin`
- **Password:** `admin123`

---

## 📋 Features

### Landing Page
- **Projects Section** - Display portfolio projects with images and descriptions
- **Happy Clients Section** - Client testimonials with photos and designations
- **Contact Form** - Collect visitor inquiries (name, email, phone, city)
- **Newsletter Subscription** - Email subscription for updates

### Admin Panel
- **Secure Login** - JWT-based authentication
- **Project Management** - Create, edit, delete projects with image upload
- **Client Management** - Manage client testimonials with image upload
- **Contact Submissions** - View all contact form entries
- **Newsletter List** - View all newsletter subscribers
- **Image Auto-Crop** - Images automatically cropped to 450x350 pixels

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python 3.11) |
| Database | MongoDB Atlas (Free Tier) |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Authentication | JWT Tokens |
| Image Processing | Pillow (PIL) |
| Web Server | Nginx (Reverse Proxy) |
| Containerization | Docker & Docker Compose |

---

## 📁 Project Structure

```
UFM/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config.py            # Environment configuration
│   │   ├── database.py          # MongoDB connection
│   │   ├── models/              # Pydantic data models
│   │   ├── routers/             # API route handlers
│   │   ├── auth/                # JWT authentication
│   │   ├── utils/               # Image processing utilities
│   │   └── static/uploads/      # Uploaded images storage
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── index.html               # Landing page
│   ├── admin.html               # Admin panel
│   ├── css/
│   │   ├── style.css            # Landing page styles
│   │   └── admin.css            # Admin panel styles
│   └── js/
│       ├── api.js               # API client
│       ├── main.js              # Landing page logic
│       └── admin.js             # Admin panel logic
├── nginx/
│   └── nginx.conf               # Reverse proxy configuration
├── docker-compose.yml           # Container orchestration
├── .env.example                 # Environment template
└── README.md
```

---

## 🔌 API Endpoints

### Public Endpoints (No Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | Get all projects |
| GET | `/api/projects/{id}` | Get project by ID |
| GET | `/api/clients` | Get all clients |
| POST | `/api/contact` | Submit contact form |
| POST | `/api/newsletter` | Subscribe to newsletter |

### Admin Endpoints (JWT Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/auth/login` | Login and get JWT token |
| GET | `/api/admin/auth/verify` | Verify JWT token |
| POST | `/api/admin/projects` | Create new project |
| PUT | `/api/admin/projects/{id}` | Update project |
| DELETE | `/api/admin/projects/{id}` | Delete project |
| POST | `/api/admin/clients` | Create new client |
| PUT | `/api/admin/clients/{id}` | Update client |
| DELETE | `/api/admin/clients/{id}` | Delete client |
| GET | `/api/admin/contacts` | Get all contact submissions |
| GET | `/api/admin/newsletters` | Get all newsletter subscriptions |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/seed/populate` | Populate sample data |
| POST | `/api/seed/reset` | Clear and reseed database |

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# MongoDB Connection (Atlas)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ufm_db?retryWrites=true&w=majority

# JWT Secret (change in production!)
JWT_SECRET_KEY=your-secret-key-change-in-production

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# CORS Settings
CORS_ORIGINS=http://localhost

# Image Upload Settings
UPLOAD_DIR=static/uploads
IMAGE_CROP_WIDTH=450
IMAGE_CROP_HEIGHT=350
```

### Setting Up Your Own MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a free account
2. Create a new **Free Tier Cluster**
3. Click **Database Access** → Add a new database user
4. Click **Network Access** → Add IP `0.0.0.0/0` (allows all IPs for development)
5. Click **Connect** → Choose **Drivers** → Copy the connection string
6. Replace `<password>` with your database user's password
7. Update `MONGODB_URI` in your `.env` file

**Note:** If your password contains special characters like `@`, you need to URL-encode them:
- `@` → `%40`
- `#` → `%23`
- `$` → `%24`

---

## 🖥️ Development

### Running Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (using Python):**
```bash
cd frontend
python -m http.server 8080
```

Access at: http://localhost:8080 (frontend) and http://localhost:8000/docs (API)

---

## 🧪 Testing the Application

### 1. Test Landing Page
- Open http://localhost
- Verify projects and clients are displayed
- Submit a contact form
- Subscribe to newsletter

### 2. Test Admin Panel
- Open http://localhost/admin.html
- Login with `admin` / `admin123`
- Create a new project with image upload
- Edit and delete projects
- View contacts and newsletters

### 3. Test API (Swagger)
- Open http://localhost/docs
- Click "Authorize" button
- First call `/api/admin/auth/login` with credentials
- Copy the `access_token` from response
- Paste token in Authorize dialog
- Test protected endpoints

---

## 🔧 Common Commands

```bash
# Start application
docker-compose up -d

# Start with rebuild
docker-compose up --build -d

# View logs
docker-compose logs -f

# View backend logs only
docker-compose logs -f backend

# Stop application
docker-compose down

# Restart application
docker-compose restart

# Reset database with fresh sample data
curl -X POST http://localhost/api/seed/reset
# PowerShell: Invoke-WebRequest -Uri "http://localhost/api/seed/reset" -Method POST
```

---

## ❓ Troubleshooting

### Application Not Starting

```bash
# Check if containers are running
docker-compose ps

# Check logs for errors
docker-compose logs backend
docker-compose logs nginx
```

### MongoDB Connection Error

- Verify your MongoDB Atlas connection string is correct
- Check that your IP is whitelisted in MongoDB Atlas (Network Access)
- Ensure password special characters are URL-encoded
- Test connection string format: `mongodb+srv://user:password@cluster.mongodb.net/dbname`

### Port 80 Already in Use

```bash
# Windows - find what's using port 80
netstat -ano | findstr :80

# Stop the process or change port in docker-compose.yml
```

### Images Not Loading After Upload

```bash
# Restart containers
docker-compose restart

# Or rebuild completely
docker-compose down
docker-compose up --build -d
```

### Admin Login Not Working

- Default credentials: `admin` / `admin123`
- Clear browser localStorage: Open DevTools → Application → Local Storage → Clear
- Check `.env` file has correct `ADMIN_USERNAME` and `ADMIN_PASSWORD`

### Clear All Data and Start Fresh

```bash
# Reset database
curl -X POST http://localhost/api/seed/reset

# Or completely rebuild
docker-compose down -v
docker-compose up --build -d
```

---

## 📝 Notes

- **Single Port Architecture**: Both frontend and backend run on port 80 via Nginx reverse proxy
- **Image Processing**: All uploaded images are automatically cropped to 450x350 pixels
- **Seed Data**: Uses Unsplash images for sample projects and clients
- **JWT Expiration**: Tokens expire after 24 hours

---

## 📄 License

This project is created for the FLIPR Placement Drive Assessment.

---

## 👨‍💻 Author

Created as part of the Full Stack Development Assessment Task.
