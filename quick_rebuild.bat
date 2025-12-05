@echo off
REM Quick Docker Build Script (uses cache for speed)
REM Use this for rebuilds after code changes

echo ========================================
echo Quick Docker Build (with cache)
echo ========================================
echo.

echo Stopping services...
docker-compose down
echo.

echo Building with cache (much faster)...
docker-compose build
echo.

echo Starting services...
docker-compose up -d
echo.

echo Checking status...
timeout /t 3 /nobreak >nul
docker-compose ps
echo.

echo ========================================
echo Services should be available at:
echo   - API: http://localhost:8000/docs
echo   - UI: http://localhost:8501
echo   - Airflow: http://localhost:8080
echo ========================================
echo.
pause
