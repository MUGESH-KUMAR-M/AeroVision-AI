# AeroVision AI - Windows Setup Script
Write-Host "AeroVision AI - Setup" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Virtual environment
if (-not (Test-Path "aerovision_env")) {
    Write-Host "`n[1/5] Creating virtual environment..."
    python -m venv aerovision_env
} else {
    Write-Host "`n[1/5] Virtual environment already exists"
}

Write-Host "[2/5] Activating environment and installing packages..."
& ".\aerovision_env\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "[3/5] Creating folders..."
New-Item -ItemType Directory -Force -Path "static\uploads", "static\results", "notebooks", "runs\aerovision" | Out-Null

Write-Host "[4/5] Downloading NEU-DET dataset (may take several minutes)..."
python download_dataset.py

Write-Host "[5/5] Verifying imports..."
python -c "from ultralytics import YOLO; import cv2, flask; print('All packages OK')"

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "Train:  python train.py"
Write-Host "Web UI: python app.py  -> http://localhost:5000"
