#!/bin/bash

# Nordic Charge Pricing App Deployment Script
# Usage: ./deploy.sh

set -e  # Exit on any error

echo "🚀 Deploying Nordic Charge Pricing App..."

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Build Docker image
echo "🐳 Building Docker image..."
docker-compose build --no-cache

# Stop existing container
echo "🛑 Stopping existing container..."
docker-compose down

# Start new container
echo "▶️ Starting new container..."
docker-compose up -d

# Wait for health check
echo "🏥 Waiting for health check..."
sleep 30

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Deployment successful!"
    echo "🌐 App is running at: http://$(curl -s ifconfig.me):8501"
    echo "📊 Local access: http://localhost:8501"
else
    echo "❌ Deployment failed!"
    echo "📋 Checking logs..."
    docker-compose logs
    exit 1
fi

echo "🎉 Nordic Charge Pricing App is live!"
