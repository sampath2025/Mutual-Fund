# Mutual Fund NAV Tracker - Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Mutual Fund NAV Tracker - Starting App" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Checking Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Start backend server
Write-Host "Starting backend server on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python run_backend.py"

# Wait for backend to start
Start-Sleep -Seconds 3

# Navigate to frontend
Set-Location frontend

# Install frontend dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
}

# Start frontend server
Write-Host "Starting frontend server on http://localhost:3000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Servers are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "The app will open in your browser shortly..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop servers" -ForegroundColor Gray

# Wait a bit then open browser
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"

