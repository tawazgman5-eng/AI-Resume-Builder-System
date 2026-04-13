@echo off
title AI Resume Builder - Auto Startup

echo ==========================================
echo   Starting AI Resume Builder...
echo   Activating virtual environment
echo ==========================================

REM Move into project directory
cd /d "%~dp0"

REM Activate venv
call venv\Scripts\activate

if %errorlevel% neq 0 (
    echo ❌ ERROR: Could not activate virtual environment.
    pause
    exit /b
)

echo.
echo ✅ Virtual environment activated.
echo.

REM Start Flask server
echo 🚀 Launching Flask application...
start "" python app.py

REM Optional: auto-open browser
timeout /t 3 > nul
start "" http://127.0.0.1:5000/

echo.
echo ==========================================
echo  Flask started. You may close this window.
echo ==========================================
pause > nul
