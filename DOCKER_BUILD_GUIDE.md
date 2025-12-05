# Docker Build Quick Reference

## Files Updated ✅
- `requirements.txt` - Fixed with pinned versions
- `docker/Dockerfile.api` - Optimized build process
- `docker/Dockerfile.agent` - Optimized build process
- `docker/Dockerfile.trainer` - Optimized build process
- `docker/Dockerfile.ui` - Optimized build process
- `docker/Dockerfile.airflow` - Optimized build process
- `docker/.dockerignore` - Added to reduce build context

## Quick Start

### Windows
```bash
# Run the build script
build_docker.bat

# OR manually:
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Linux/Mac
```bash
# Make script executable
chmod +x build_docker.sh

# Run the build script
./build_docker.sh

# OR manually:
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Key Changes Made

### 1. requirements.txt
- Added version pinning to ALL packages
- Fixed version conflicts (pydantic, langchain, etc.)
- Organized by category for better maintenance

### 2. All Dockerfiles
- Added `pip install --upgrade pip setuptools wheel`
- Install PyTorch separately first (largest package)
- Batched installations to prevent timeouts
- Increased timeout to 500 seconds
- Added `--no-cache-dir` to reduce memory usage

### 3. Build Optimization
- PyTorch installed first (2GB+)
- Transformers ecosystem second
- LangChain packages third
- Everything else last
- Each batch has its own RUN command for better layer caching

## Verify Installation

After build completes, check services:
```bash
# Check all services
docker-compose ps

# Expected status:
# api-service       Up      0.0.0.0:8000->8000/tcp
# ui-service        Up      0.0.0.0:8501->8501/tcp
# agent-service     Up
# redis             Up      0.0.0.0:6379->6379/tcp
# airflow           Up      0.0.0.0:8080->8080/tcp
# trainer-service   Exited  (normal - runs once)
```

Test endpoints:
```bash
# Test API
curl http://localhost:8000/health
curl http://localhost:8000/docs

# Test UI - Open in browser
http://localhost:8501

# Test Airflow - Open in browser
http://localhost:8080
# Login: admin / admin
```

## Common Issues & Solutions

### Issue: Build still failing
```bash
# Check which service is failing
docker-compose build api 2>&1 | tee build.log

# Build one service at a time
docker-compose build api
docker-compose build agent
docker-compose build trainer
docker-compose build ui
docker-compose build airflow
```

### Issue: Out of memory
```bash
# Increase Docker memory in Docker Desktop
# Settings > Resources > Memory: 8GB minimum

# Or limit services
docker-compose up -d api ui redis
```

### Issue: Network timeout
```bash
# If you're behind a proxy, add to Dockerfile:
ENV HTTP_PROXY=http://your-proxy:port
ENV HTTPS_PROXY=http://your-proxy:port

# Or increase timeout further in Dockerfiles
--default-timeout=1000
```

### Issue: Permission denied
```bash
# Windows: Run as Administrator
# Linux/Mac: 
sudo docker-compose build
```

## Individual Service Commands

```bash
# Build specific service
docker-compose build api

# Start specific service
docker-compose up -d api

# View logs
docker-compose logs -f api

# Restart service
docker-compose restart api

# Stop service
docker-compose stop api

# Remove service
docker-compose rm -f api
```

## Clean Start (Nuclear Option)

If everything fails, completely reset:
```bash
# Stop everything
docker-compose down -v

# Remove ALL Docker data (WARNING: removes all containers/images)
docker system prune -a --volumes -f

# Rebuild
docker-compose build --no-cache

# Start
docker-compose up -d
```

## Resource Requirements

Minimum:
- RAM: 8GB
- Disk: 20GB free
- CPU: 4 cores

Recommended:
- RAM: 16GB
- Disk: 50GB free
- CPU: 8 cores

## Build Time Estimates

- API service: 5-8 minutes
- Agent service: 5-8 minutes
- Trainer service: 10-15 minutes (largest)
- UI service: 2-3 minutes
- Airflow service: 3-5 minutes
- Total: 25-40 minutes (first build)

Subsequent builds (with cache): 2-5 minutes per service

## Need Help?

Check logs for specific errors:
```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs api

# Follow logs (live)
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100 api
```

## Version Information

- Python: 3.11
- PyTorch: 2.3.1
- Transformers: 4.41.0
- LangChain: 0.2.5
- FastAPI: 0.111.0
- Airflow: 2.9.0
