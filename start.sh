#!/bin/bash

# UFM Application Startup Script

echo "========================================="
echo "UFM Full Stack Application"
echo "========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created. Please update it with your credentials."
        echo ""
        echo "Required configuration:"
        echo "  - MONGODB_URI: Your MongoDB Atlas connection string"
        echo "  - JWT_SECRET_KEY: A secret key for JWT tokens"
        echo "  - GOOGLE_CLIENT_ID: Your Google OAuth Client ID"
        echo "  - GOOGLE_CLIENT_SECRET: Your Google OAuth Client Secret"
        echo ""
        read -p "Press Enter after updating .env file to continue..."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🚀 Starting application with Docker Compose..."
echo ""

# Build and start containers
docker-compose up --build -d

echo ""
echo "✅ Application is starting!"
echo ""
echo "Access the application at:"
echo "  - Frontend: http://localhost"
echo "  - Admin Panel: http://localhost/admin.html"
echo "  - API: http://localhost/api"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""

