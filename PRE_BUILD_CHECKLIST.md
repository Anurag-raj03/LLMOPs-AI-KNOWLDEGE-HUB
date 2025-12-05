# ✅ Pre-Build Checklist

Before running `docker-compose build`, verify these requirements:

## System Requirements

### Hardware
- [ ] RAM: 8GB minimum (16GB recommended)
- [ ] Disk Space: 20GB free minimum (50GB recommended)
- [ ] CPU: 4 cores minimum (8 cores recommended)

### Software
- [ ] Docker Desktop installed and running
- [ ] Docker version 20.10+ (`docker --version`)
- [ ] Docker Compose version 2.0+ (`docker-compose --version`)
- [ ] Internet connection stable (will download ~3GB)

## Docker Settings (Docker Desktop)

### Memory
- [ ] Open Docker Desktop > Settings > Resources > Memory
- [ ] Set to **8GB minimum** (16GB if available)
- [ ] Click "Apply & Restart"

### Disk Space
- [ ] Docker Desktop > Settings > Resources > Disk image size
- [ ] Ensure at least 20GB allocated
- [ ] Click "Apply & Restart"

## File Verification

- [ ] `requirements.txt` exists and has version numbers (1.13 KB)
- [ ] `docker/Dockerfile.api` has been updated (1.07 KB)
- [ ] `docker/Dockerfile.agent` has been updated (1.01 KB)
- [ ] `docker/Dockerfile.trainer` has been updated (1.50 KB)
- [ ] `docker/Dockerfile.ui` has been updated (437 B)
- [ ] `docker/Dockerfile.airflow` has been updated (1.06 KB)
- [ ] `docker/.dockerignore` exists (590 B)

## Clean State (Optional but Recommended)

- [ ] Stop all running containers: `docker-compose down -v`
- [ ] Remove old builds: `docker system prune -f` (optional)
- [ ] Close other resource-heavy applications

## Network

- [ ] Internet connection is stable
- [ ] Not behind a restrictive firewall
- [ ] Can access PyPI (pip package repository)
- [ ] Can access Docker Hub

## Environment

- [ ] `.env` file exists in project root
- [ ] No conflicting processes on ports 8000, 8501, 8080, 6379
- [ ] Running terminal/command prompt as Administrator (Windows) or with sudo (Linux)

## Ready to Build?

### Quick Test (before full build):
```bash
# Test Docker is working
docker --version
docker-compose --version

# Test Docker can pull images
docker pull python:3.11-slim

# Test Docker can run
docker run --rm python:3.11-slim python --version
```

If all tests pass, proceed with build:

### Windows:
```bash
build_docker.bat
```

### Linux/Mac:
```bash
chmod +x build_docker.sh
./build_docker.sh
```

### Manual:
```bash
docker-compose build --no-cache
docker-compose up -d
```

## Post-Build Verification

After build completes (25-40 minutes), verify:

- [ ] All services are "Up" (except trainer which should be "Exited 0")
- [ ] No error messages in logs
- [ ] Can access http://localhost:8000/docs
- [ ] Can access http://localhost:8501
- [ ] Can access http://localhost:8080

Run verification:
```bash
docker-compose ps
docker-compose logs | grep -i error
curl http://localhost:8000/health
```

## Common Issues Checklist

If build fails, check:

- [ ] Docker has enough memory (8GB+)
- [ ] Sufficient disk space (20GB+)
- [ ] Internet connection didn't drop
- [ ] No other process using ports 8000, 8501, 8080, 6379
- [ ] Docker Desktop is running
- [ ] Reviewed error logs: `docker-compose logs`

## Need Help?

1. Check `DOCKER_BUILD_GUIDE.md` for detailed troubleshooting
2. Review `UPDATE_SUMMARY.md` for what was changed
3. Check logs: `docker-compose logs [service-name]`
4. Build one service at a time to isolate issues:
   ```bash
   docker-compose build api
   docker-compose build agent
   docker-compose build trainer
   docker-compose build ui
   docker-compose build airflow
   ```

---

✅ **All checks passed?** → Run the build script!

❌ **Some checks failed?** → Fix issues first, then try again

🆘 **Still stuck?** → Check logs and `DOCKER_BUILD_GUIDE.md`
