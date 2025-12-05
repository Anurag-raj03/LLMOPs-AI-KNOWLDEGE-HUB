# Current Build Issues - TROUBLESHOOTING

## Issue 1: Airflow Dependency Conflicts ✅ FIXED

**Error seen:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
snowflake-connector-python 3.7.1 requires cffi<2.0.0,>=1.9, but you have cffi 2.0.0 which is incompatible.
gcsfs 2023.12.2.post1 requires fsspec==2023.12.2, but you have fsspec 2025.10.0 which is incompatible.
```

**Solution Applied:**
- Updated `orchestrator/requirements.txt` with compatible versions
- Changed Dockerfile.airflow to install packages in specific order
- Using apache-airflow==2.9.2 as base (matches requirements)

**Status:** ✅ Airflow service built successfully (as shown in logs)

## Issue 2: Very Slow PyTorch Download

**Observed:**
- PyTorch (779MB) taking 8-11 minutes to download
- CUDA libraries (410MB, 731MB) taking 4-7 minutes each
- Total: 15-20 minutes per service just for PyTorch

**This is NORMAL** - these are large packages:
- torch: 779 MB
- nvidia_cudnn_cu12: 731 MB  
- nvidia_cublas_cu12: 410 MB
- Total: ~2GB per service

**Not an error - just slow internet/PyPI servers**

## Issue 3: Pydantic Backtracking (Taking Too Long)

**Error:**
```
pip is looking at multiple versions of pydantic to determine which version is compatible
This is taking longer than usual. You might need to provide stricter constraints
```

**Solution Applied:**
- Pinned pydantic==2.7.4 in main requirements.txt
- Separated Airflow's pydantic needs from main project
- Airflow uses older pydantic==2.6.4 (comes with base image)

## Current Build Status (Based on Your Logs)

✅ **Airflow** - COMPLETED (built in ~1135 seconds = 19 minutes)
🔄 **API** - STILL BUILDING (at PyTorch download, ~1310 seconds in)
🔄 **Agent** - STILL BUILDING (at PyTorch download)
🔄 **Trainer** - STILL BUILDING (at PyTorch download)

## What To Do Now

### Option 1: Let Current Build Complete (Recommended)
The build is progressing normally. Just wait:
- API service: ~10 more minutes
- Agent service: ~10 more minutes  
- Trainer service: ~15 more minutes

**Total remaining: ~35 minutes**

Watch progress:
```bash
docker-compose build --progress=plain 2>&1 | tee build.log
```

### Option 2: Cancel and Use Optimized Build

If you want better control:

1. **Stop current build:**
   - Press `Ctrl+C`

2. **Run optimized build:**
   ```bash
   build_docker_optimized.bat
   ```
   
   This builds one service at a time with error checking.

### Option 3: Skip Trainer Service (Fastest)

Trainer takes longest and may not be needed immediately:

1. **Edit docker-compose.yaml** - Trainer is already commented out
2. **Build without trainer:**
   ```bash
   docker-compose build api agent ui airflow
   docker-compose up -d
   ```

## Expected Total Build Times

| Service  | Download | Build | Total    |
|----------|----------|-------|----------|
| Redis    | 0 min    | 0 min | 0 min    |
| API      | 10 min   | 5 min | 15 min   |
| Agent    | 10 min   | 5 min | 15 min   |
| Trainer  | 12 min   | 8 min | 20 min   |
| UI       | 1 min    | 2 min | 3 min    |
| Airflow  | 5 min    | 14 min| 19 min   |
| **Total**|          |       | **~70 min**|

*First build only. Rebuilds use cache: 2-5 minutes*

## Progress Indicators

### ✅ Good Signs (from your logs):
- Airflow built successfully
- Downloads progressing (even if slow)
- No actual errors in package installation
- Services showing proper download progress bars

### ⚠️ Warning Signs to Watch For:
- "ERROR" messages in build output
- Build hanging for >30 minutes on same step
- Network timeout errors
- Out of memory errors

## Monitor Build Progress

Open another terminal and run:
```bash
# See which containers are building
docker ps -a

# Watch logs live
docker-compose logs -f

# Check disk space
docker system df
```

## After Build Completes

Verify all services:
```bash
# Check status
docker-compose ps

# Expected output:
# api        Up      0.0.0.0:8000->8000/tcp
# ui         Up      0.0.0.0:8501->8501/tcp  
# agent      Up
# airflow    Up      0.0.0.0:8080->8080/tcp
# redis      Up      0.0.0.0:6379->6379/tcp

# Test services
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

Open in browser:
- http://localhost:8501 (UI)
- http://localhost:8080 (Airflow - admin/admin)

## If Build Fails

1. **Check which service failed:**
   ```bash
   docker-compose ps -a
   ```

2. **View error logs:**
   ```bash
   docker-compose logs [failed-service]
   ```

3. **Rebuild just that service:**
   ```bash
   docker-compose build [failed-service]
   ```

4. **Common fixes:**
   - Increase Docker memory to 8GB+
   - Free up disk space (20GB+ needed)
   - Check internet connection
   - Try again later (PyPI can be slow)

## Summary

**Your build is working correctly!** 

The main "issue" is just slow downloads due to:
1. Large packages (PyTorch = 2GB+ per service)
2. PyPI server speed
3. Your internet connection speed

**Recommendation:** Let the current build complete. It should finish in ~30-40 more minutes.

All dependency conflicts have been fixed in the updated files.
