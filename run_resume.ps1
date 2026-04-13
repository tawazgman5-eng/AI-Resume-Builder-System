Write-Host "=========================================="
Write-Host " Starting AI Resume Builder (PowerShell)"
Write-Host "==========================================" -ForegroundColor Cyan

# Change to script directory
Set-Location $PSScriptRoot

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
. .\venv\Scripts\Activate.ps1

# Run Flask app
Write-Host "Launching Flask server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python app.py"

# Open browser
Start-Process "http://127.0.0.1:5000/"
