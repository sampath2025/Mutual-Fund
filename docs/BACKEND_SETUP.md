# 🐍 Python Backend Setup Guide

## Overview

The backend is built with **Python 3.9+** using:
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Default database (can switch to PostgreSQL)
- **Uvicorn** - ASGI server

## ✨ Features Added

### 1. Database Integration
- **SQLite** database for persistence (default)
- **PostgreSQL** support (configurable)
- Models for Funds, Alerts, and NAV History
- Automatic database initialization

### 2. Configuration Management
- Environment variable support (`.env` file)
- Centralized configuration (`src/config.py`)
- Configurable email, database, and agent settings

### 3. Service Layer
- **FundService** - Fund CRUD operations
- **AlertService** - Alert management
- Database persistence for all operations

### 4. Health Checks
- `/health` - Basic health check
- `/health/detailed` - Detailed system status

## 🚀 Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install Python packages
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

Create a `.env` file in the project root:

```env
# API Configuration
API_TITLE=Mutual Fund NAV Tracker API
API_VERSION=1.0.0
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Database
DATABASE_URL=sqlite:///./mutual_fund_tracker.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname

# Agent Configuration
AGENT_CHECK_INTERVAL=300  # 5 minutes in seconds
ALERT_COOLDOWN_HOURS=1

# Email Configuration
EMAIL_ENABLED=False
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECEIVER_EMAIL=recipient@example.com

# Logging
LOG_LEVEL=INFO
```

### 3. Run the Backend

```bash
python run_backend.py
```

Or using uvicorn directly:

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Database Schema

### Funds Table
- `id` - Primary key
- `scheme_code` - Unique scheme code
- `scheme_name` - Fund name
- `fund_house` - Fund house name
- `category` - Fund category
- `alert_threshold` - Alert threshold percentage
- `is_active` - Active status
- `created_at`, `updated_at` - Timestamps

### Alerts Table
- `id` - Primary key
- `scheme_code` - Fund scheme code
- `scheme_name` - Fund name
- `timestamp` - Alert time
- `drop_percentage` - NAV drop percentage
- `current_nav`, `previous_nav` - NAV values
- `message` - Alert message
- `severity` - Alert severity
- `acknowledged` - Acknowledgment status

### NAV History Table
- `id` - Primary key
- `scheme_code` - Fund scheme code
- `date` - NAV date
- `nav` - NAV value
- `created_at` - Record creation time

## 🔌 API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status

### Funds
- `GET /api/funds` - List all funds (from database)
- `POST /api/funds` - Add fund (saves to database)
- `DELETE /api/funds/{scheme_code}` - Remove fund (from database)

### Alerts
- `GET /api/alerts` - Get alerts (from database)
- `GET /api/alerts?scheme_code=XXX` - Filter by scheme code

### Other Endpoints
- All existing endpoints remain the same
- Database integration is transparent to the frontend

## 🗄️ Database Operations

### Using the Services

```python
from src.database import get_db
from src.services.fund_service import FundService
from src.services.alert_service import AlertService

# Get database session
db = next(get_db())

# Create a fund
fund = Fund(...)
db_fund = FundService.create_fund(db, fund)

# Get all funds
funds = FundService.get_all_funds(db)

# Get alerts
alerts = AlertService.get_alerts(db, limit=50)
```

## 🔧 Configuration Options

### Database
- **SQLite** (default): `sqlite:///./mutual_fund_tracker.db`
- **PostgreSQL**: `postgresql://user:pass@host/dbname`

### Agent Settings
- `AGENT_CHECK_INTERVAL` - How often to check NAVs (seconds)
- `ALERT_COOLDOWN_HOURS` - Time between alerts for same fund

### Email Settings
- Configure SMTP settings in `.env`
- Set `EMAIL_ENABLED=True` to enable

## 📝 Migration Notes

### Existing Data
- Funds added via API are now persisted to database
- Alerts are saved automatically
- NAV history can be stored (optional)

### Backward Compatibility
- All existing API endpoints work the same
- Frontend doesn't need changes
- Database is optional (can run without it)

## 🐛 Troubleshooting

### Database Errors
```bash
# Delete database to reset
rm mutual_fund_tracker.db  # Linux/Mac
del mutual_fund_tracker.db  # Windows
```

### Import Errors
```bash
# Make sure you're in project root
cd "C:\Users\suman\Downloads\Mutual Fund"
python run_backend.py
```

### Port Already in Use
```bash
# Change port in .env or run_backend.py
API_PORT=8001
```

## ✅ Verification

1. **Check Health**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check Database**:
   - SQLite file: `mutual_fund_tracker.db`
   - Should be created automatically

3. **Check Logs**:
   - Backend logs show database initialization
   - Check for "Database initialized successfully"

## 🎯 Next Steps

1. **Add Funds**: Use API to add funds (they're saved to DB)
2. **View Alerts**: Alerts are persisted in database
3. **Monitor**: Check `/health/detailed` for system status
4. **Configure**: Customize settings in `.env`

---

**Your Python backend is now fully set up with database support! 🚀**

