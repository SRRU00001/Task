@echo off
REM UFM Application Startup Script for Windows

echo =========================================
echo UFM Full Stack Application
echo =========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo Creating .env from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo ✅ .env file created. Please update it with your credentials.
        echo.
        echo Required configuration:
        echo   - MONGODB_URI: Your MongoDB Atlas connection string
        echo   - JWT_SECRET_KEY: A secret key for JWT tokens
        echo   - GOOGLE_CLIENT_ID: Your Google OAuth Client ID
        echo   - GOOGLE_CLIENT_SECRET: Your Google OAuth Client Secret
        echo.
        pause
    ) else (
        echo ❌ .env.example not found. Please create .env manually.
        exit /b 1
    )
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo 🚀 Starting application with Docker Compose...
echo.

REM Build and start containers
docker-compose up --build -d

echo.
echo ✅ Application is starting!
echo.
echo Access the application at:
echo   - Frontend: http://localhost
echo   - Admin Panel: http://localhost/admin.html
echo   - API: http://localhost/api
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
echo.

pause

