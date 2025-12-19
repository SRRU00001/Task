# UFM Application Deployment Guide

This guide covers deploying the UFM application to production.

---

## Architecture for Production

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                 │
└─────────────────────────────────────────────────────────────────┘
          │                                    │
          ▼                                    ▼
┌─────────────────────┐              ┌─────────────────────┐
│   VERCEL (Free)     │              │  RAILWAY (Free)     │
│   Frontend Host     │  ──────────▶ │  Backend Host       │
│   your-app.vercel   │   API Calls  │  your-api.railway   │
│                     │              │                     │
│   - index.html      │              │   - FastAPI         │
│   - admin.html      │              │   - Image uploads   │
│   - CSS/JS files    │              │   - Static files    │
└─────────────────────┘              └─────────────────────┘
                                              │
                                              ▼
                                     ┌─────────────────────┐
                                     │  MONGODB ATLAS      │
                                     │  (Free Tier)        │
                                     │  Cloud Database     │
                                     └─────────────────────┘
```

---

## Step 1: Deploy Backend on Railway

Railway offers free tier with 500 hours/month and $5 credit.

### 1.1 Prepare Backend for Railway

Create a `railway.json` in the `backend/` folder:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 1.2 Deploy to Railway

1. **Sign up** at [railway.app](https://railway.app) using GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository

3. **Configure Root Directory**:
   - Go to Settings → General
   - Set "Root Directory" to `backend`

4. **Add Environment Variables**:
   Go to Variables tab and add:

   | Variable | Value |
   |----------|-------|
   | `MONGODB_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/ufm_db` |
   | `JWT_SECRET_KEY` | `your-super-secret-key-change-this` |
   | `ADMIN_USERNAME` | `admin` |
   | `ADMIN_PASSWORD` | `your-secure-password` |
   | `CORS_ORIGINS` | `https://your-app.vercel.app` |
   | `UPLOAD_DIR` | `static/uploads` |
   | `IMAGE_CROP_WIDTH` | `450` |
   | `IMAGE_CROP_HEIGHT` | `350` |

5. **Deploy**:
   - Railway will auto-detect Dockerfile and deploy
   - Wait for deployment to complete
   - Note your URL: `https://your-project.up.railway.app`

6. **Test Backend**:
   ```bash
   curl https://your-project.up.railway.app/api/projects
   ```

---

## Step 2: Update Frontend Configuration

Edit `frontend/js/config.js`:

```javascript
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? '/api' 
        : 'https://your-project.up.railway.app/api'  // <-- Your Railway URL
};

window.CONFIG = CONFIG;
```

---

## Step 3: Deploy Frontend on Vercel

### 3.1 Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### 3.2 Deploy via Vercel Dashboard

1. **Sign up** at [vercel.com](https://vercel.com) using GitHub

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: `.` (current directory)

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment
   - Your frontend is live at: `https://your-app.vercel.app`

### 3.3 Deploy via CLI

```bash
cd frontend
vercel

# Answer prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? ufm-frontend
# - Directory? ./
# - Override settings? No
```

---

## Step 4: Update CORS on Backend

After getting your Vercel URL, update Railway environment variables:

```
CORS_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com
```

---

## Step 5: Seed Production Database

```bash
# Using curl
curl -X POST https://your-project.up.railway.app/api/seed/populate

# Using PowerShell
Invoke-WebRequest -Uri "https://your-project.up.railway.app/api/seed/populate" -Method POST
```

---

## Alternative: Deploy Backend on Render

[Render.com](https://render.com) is another free option.

### Create Web Service

1. Sign up at render.com
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   - **Name**: `ufm-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Plan**: Free

5. Add environment variables (same as Railway)

6. Deploy

---

## Alternative: Full Vercel Deployment (Serverless)

⚠️ **This requires code restructuring** - Not recommended for this project.

Vercel can run Python as serverless functions, but:
- No persistent file storage (need Cloudinary/S3 for images)
- Cold starts may be slow
- Requires converting to API routes format

If you want this approach, you would need to:

1. Create `api/` folder with Python files
2. Use Cloudinary for image uploads
3. Restructure routes to Vercel serverless format

---

## Production Checklist

### Security
- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Change `ADMIN_PASSWORD` to a strong password
- [ ] Enable HTTPS (automatic on Vercel/Railway)
- [ ] Set proper CORS_ORIGINS (not wildcard)

### MongoDB Atlas
- [ ] Create production database user
- [ ] Whitelist Railway/Render IP addresses (or 0.0.0.0/0)
- [ ] Enable MongoDB Atlas monitoring

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Enable logging on Railway/Render
- [ ] Set up uptime monitoring (UptimeRobot)

---

## Custom Domain Setup

### Vercel (Frontend)
1. Go to Project Settings → Domains
2. Add your domain: `www.yourdomain.com`
3. Update DNS records as instructed

### Railway (Backend)
1. Go to Settings → Domains
2. Add custom domain: `api.yourdomain.com`
3. Update DNS CNAME record

Then update `frontend/js/config.js`:
```javascript
API_BASE_URL: 'https://api.yourdomain.com/api'
```

---

## Troubleshooting

### CORS Errors
- Verify `CORS_ORIGINS` includes your frontend URL
- Include both `http://` and `https://` if needed
- Check for trailing slashes

### 502 Bad Gateway on Railway
- Check logs: Railway Dashboard → Deployments → View Logs
- Verify MongoDB connection string
- Check if port is correctly bound (`$PORT` environment variable)

### Images Not Loading
- Railway's file system is ephemeral
- For production, use Cloudinary or AWS S3 for image storage
- Current setup works but images may be lost on redeploy

### MongoDB Connection Failed
- Verify connection string is correct
- Check IP whitelist in MongoDB Atlas
- Ensure password special characters are URL-encoded

---

## Cost Summary (Free Tiers)

| Service | Free Tier Limits |
|---------|------------------|
| **Vercel** | 100GB bandwidth, unlimited deploys |
| **Railway** | $5/month credit (~500 hours) |
| **Render** | 750 hours/month |
| **MongoDB Atlas** | 512MB storage, shared cluster |

For a low-traffic site, this is completely free!

---

## Quick Deploy Commands

```bash
# Deploy frontend to Vercel
cd frontend
vercel --prod

# Deploy backend to Railway
cd backend
railway up

# Seed production database
curl -X POST https://your-backend.up.railway.app/api/seed/populate
```

