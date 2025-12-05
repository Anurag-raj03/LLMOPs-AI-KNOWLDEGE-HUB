@echo off
echo ========================================
echo Docker Build - Final Run
echo ========================================
echo.
echo All dependency issues are now fixed!
echo Local environment confirmed working.
echo.

echo Stopping any running containers...
docker-compose down
echo.

echo Starting fresh build...
echo This will take 40-60 minutes for first build.
echo.

echo Building services...
docker-compose build --progress=plain
echo.

echo Starting services...
docker-compose up -d
echo.

echo Checking status...
timeout /t 5 /nobreak >nul
docker-compose ps
echo.

echo ========================================
echo Services should be available at:
echo   - API: http://localhost:8000/docs
echo   - UI: http://localhost:8501
echo   - Airflow: http://localhost:8080 (admin/admin)
echo ========================================
echo.
echo View logs: docker-compose logs -f
echo.
pause
