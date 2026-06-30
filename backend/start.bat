@echo off
echo ==========================================
echo Starting Crumbs Backend Stack...
echo ==========================================

:: 1. Check if Redis is downloaded, if not download and extract it
if not exist "Redis\redis-server.exe" (
    echo [1/4] Downloading Redis for Windows...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip' -OutFile 'Redis.zip'"
    echo [2/4] Extracting Redis...
    powershell -Command "Expand-Archive -Path 'Redis.zip' -DestinationPath 'Redis' -Force"
    del Redis.zip
) else (
    echo [1/4] Redis is already downloaded.
)

:: 2. Start Redis in a new window
echo [3/4] Starting Redis Server...
start "Redis Server" cmd /c "cd Redis && redis-server.exe"

:: 3. Start Celery in a new window
echo [4/4] Starting Celery Worker...
start "Celery Worker" cmd /c "celery -A main worker --loglevel=info -P solo"

:: 4. Start Django server in this window
echo ==========================================
echo All background services started!
echo Starting Django Web Server...
echo ==========================================
python manage.py runserver
