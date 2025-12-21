# 🚀 START HERE - Run the Web Application

## ⚡ Quick Start (3 Steps)

### 1️⃣ Start Backend Server

Open **PowerShell** or **Command Prompt** in this folder and run:

```powershell
# Activate virtual environment
venv\Scripts\activate

# Start backend (if dependencies not installed, run: pip install -r requirements.txt first)
python run_backend.py
```

**Keep this window open!** Backend runs on: http://localhost:8000

### 2️⃣ Start Frontend Server

Open a **NEW** PowerShell/Command Prompt window and run:

```powershell
cd frontend
npm run dev
```

**Keep this window open too!** Frontend runs on: http://localhost:3000

### 3️⃣ Open in Browser

Once both servers are running, open:
- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## 🎯 What You'll See

1. **Beautiful Dashboard** with gradient UI
2. **Add Funds** to track NAV
3. **Real-time Charts** showing NAV trends
4. **Alerts** when NAV drops exceed thresholds
5. **Backtesting** to test strategies

## 📝 First Time Setup

If you haven't installed dependencies yet:

### Backend:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend:
```powershell
cd frontend
npm install
```

## ✅ Verify It's Working

1. Backend: Visit http://localhost:8000 - should show API info
2. Frontend: Visit http://localhost:3000 - should show dashboard

## 🎨 Try It Out!

1. Click **"Manage Funds"** tab
2. Click **"Add Fund"**
3. Enter:
   - Scheme Code: `125497` (HDFC Equity Fund - example)
   - Scheme Name: `HDFC Equity Fund`
   - Fund House: `HDFC Mutual Fund`
   - Category: `Equity`
   - Alert Threshold: `2.0`
4. Click **"Add Fund"**
5. Go to **"Dashboard"** to see real-time NAV!

---

**That's it! Your Mutual Fund NAV Tracker is ready! 📈**

