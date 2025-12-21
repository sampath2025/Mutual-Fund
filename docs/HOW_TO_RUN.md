# 🚀 How to Run the Web Application

## Quick Start (Easiest Method)

### Option 1: Using Batch Script (Windows)
Double-click `start_app.bat` - it will:
- Set up virtual environment
- Install dependencies
- Start both servers
- Open the app in your browser

### Option 2: Using PowerShell Script
Right-click `start_app.ps1` → Run with PowerShell

### Option 3: Manual Start

#### Step 1: Start Backend Server
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start server
python run_backend.py
```
Backend will run on: **http://localhost:8000**

#### Step 2: Start Frontend Server (New Terminal)
```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Start server
npm run dev
```
Frontend will run on: **http://localhost:3000**

## 🌐 Access the Application

Once both servers are running:

- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000

## ✅ Verify Servers Are Running

### Check Backend
Open browser: http://localhost:8000
You should see: `{"message": "Mutual Fund NAV Tracker API", ...}`

### Check Frontend
Open browser: http://localhost:3000
You should see the dashboard interface

## 🐛 Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check Python version: `python --version` (needs 3.9+)
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Make sure port 3000 is not in use
- Install dependencies: `cd frontend && npm install`
- Clear cache: `rm -rf node_modules && npm install`

### "Module not found" errors
- Backend: `pip install -r requirements.txt`
- Frontend: `cd frontend && npm install`

### Port already in use
- Change port in `run_backend.py` (line 10) for backend
- Change port in `frontend/vite.config.js` (line 7) for frontend

## 📱 First Steps After Launch

1. **Add a Fund**:
   - Go to "Manage Funds" tab
   - Click "Add Fund"
   - Enter scheme code (e.g., `125497` for HDFC Equity Fund)
   - Set alert threshold (default: 2%)

2. **View Dashboard**:
   - See real-time NAV updates
   - View 30-day charts

3. **Test Backtesting**:
   - Go to "Backtest" tab
   - Enter scheme code and threshold
   - Click "Run Backtest"

## 🎯 Example Scheme Codes

- HDFC Equity Fund: `125497`
- SBI Bluechip Fund: `120465`
- ICICI Prudential Technology: `120465`

Find more at: https://www.mfapi.in/

---

**Happy Tracking! 📈**

