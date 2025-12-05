#!/bin/bash
# Docker Build Script for AIops Project
# Run this script to rebuild your Docker containers with fixed dependencies

echo "========================================"
echo "AIops Docker Build Script"
echo "========================================"
echo ""

echo "Step 1: Stopping all running containers..."
docker-compose down -v
echo ""

echo "Step 2: Removing old images (this will free up space)..."
read -p "Press Enter to continue or Ctrl+C to skip..."
docker system prune -a -f
echo ""

echo "Step 3: Building containers (this may take 15-30 minutes)..."
echo "Building with no cache to ensure clean build..."
docker-compose build --no-cache --progress=plain
echo ""

echo "Step 4: Starting services..."
docker-compose up -d
echo ""

echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Services should be available at:"
echo "  - API: http://localhost:8000"
echo "  - UI: http://localhost:8501"
echo "  - Airflow: http://localhost:8080 (admin/admin)"
echo "  - Redis: localhost:6379"
echo ""
echo "Check service status with: docker-compose ps"
echo "View logs with: docker-compose logs -f [service-name]"
echo ""
