#!/bin/bash

# Deployment script for Cron Job API

echo "🚀 Starting deployment..."

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🏗️  Building and starting containers..."
docker-compose up -d --build

# Show logs
echo "📋 Showing logs..."
docker-compose logs -f --tail=50
