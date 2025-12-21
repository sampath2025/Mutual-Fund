@echo off
echo ========================================
echo Mutual Fund NAV Tracker - Starting App
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies if needed
echo Checking Python dependencies...
pip install -r requirements.txt --quiet

REM Start backend server in new window
echo Starting backend server on http://localhost:8000...
start "Backend Server" cmd /k "python run_backend.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Navigate to frontend and install dependencies if needed
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend server in new window
echo Starting frontend server on http://localhost:3000...
start "Frontend Server" cmd /k "npm run dev"

cd ..

echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
echo (Servers will continue running in separate windows)
pause >nul

