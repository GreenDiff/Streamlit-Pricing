#!/bin/bash

# Nordic Charge Pricing App Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on any error

echo "🚀 Deploying Nordic Charge Pricing App..."

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Copy dockerignore to root for build context
echo "📋 Setting up Docker context..."
cp docker/dockerignore .dockerignore

# Build Docker image using docker folder
echo "🐳 Building Docker image..."
docker-compose -f docker/docker-compose.yml build --no-cache

# Stop existing container
echo "🛑 Stopping existing container..."
docker-compose -f docker/docker-compose.yml down

# Start new container
echo "▶️ Starting new container..."
docker-compose -f docker/docker-compose.yml up -d

# Wait for health check
echo "🏥 Waiting for health check..."
sleep 30

# Check if container is running
if docker-compose -f docker/docker-compose.yml ps | grep -q "Up"; then
    echo "✅ Deployment successful!"
    echo "🌐 App is running at: http://$(curl -s ifconfig.me):8501"
    echo "📊 Local access: http://localhost:8501"
else
    echo "❌ Deployment failed!"
    echo "📋 Checking logs..."
    docker-compose -f docker/docker-compose.yml logs
    exit 1
fi

echo "🎉 Nordic Charge Pricing App is live!"
