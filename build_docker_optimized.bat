@echo off
REM Optimized Docker Build Script for AIops Project
REM This builds services one at a time to manage resources better

echo ========================================
echo AIops Optimized Docker Build Script
echo ========================================
echo.
echo This will build services individually to save resources
echo Trainer service is DISABLED by default (takes longest)
echo.

REM Stop all services
echo Step 1: Stopping all running containers...
docker-compose down -v
echo.

REM Optional cleanup
echo Step 2: Clean old images? (Press Ctrl+C to skip, Enter to continue)
pause
docker system prune -f
echo.

REM Build services in order of dependency
echo ========================================
echo Building Services (this will take time)
echo ========================================
echo.

echo [1/5] Building Redis (using pre-built image)...
docker-compose pull redis
echo.

echo [2/5] Building API service (~10 minutes)...
docker-compose build --no-cache api
if errorlevel 1 (
    echo ERROR: API build failed!
    pause
    exit /b 1
)
echo ✓ API service built successfully
echo.

echo [3/5] Building UI service (~3 minutes)...
docker-compose build --no-cache ui
if errorlevel 1 (
    echo ERROR: UI build failed!
    pause
    exit /b 1
)
echo ✓ UI service built successfully
echo.

echo [4/5] Building Agent service (~10 minutes)...
docker-compose build --no-cache agent
if errorlevel 1 (
    echo ERROR: Agent build failed!
    pause
    exit /b 1
)
echo ✓ Agent service built successfully
echo.

echo [5/5] Building Airflow service (~15 minutes)...
docker-compose build --no-cache airflow
if errorlevel 1 (
    echo ERROR: Airflow build failed!
    pause
    exit /b 1
)
echo ✓ Airflow service built successfully
echo.

REM Optional: Build trainer (commented out by default)
echo.
echo NOTE: Trainer service is disabled in docker-compose.yaml
echo If you need it, uncomment it in docker-compose.yaml and run:
echo docker-compose build trainer
echo.

REM Start services
echo ========================================
echo Starting Services
echo ========================================
docker-compose up -d
echo.

REM Check status
echo ========================================
echo Build Complete! Checking Status...
echo ========================================
timeout /t 5 /nobreak >nul
docker-compose ps
echo.

echo ========================================
echo Services Available:
echo ========================================
echo   - API: http://localhost:8000/docs
echo   - UI: http://localhost:8501
echo   - Airflow: http://localhost:8080 (admin/admin)
echo   - Redis: localhost:6379
echo.
echo View logs: docker-compose logs -f [service-name]
echo Stop services: docker-compose down
echo.
pause
