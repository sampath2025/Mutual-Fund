# Project Structure

This document describes the organization of the Mutual Fund NAV Tracker project.

## 📁 Directory Structure

```
Mutual-Fund/
│
├── backend/                    # Python backend application
│   ├── src/                    # Source code
│   │   ├── agent/             # AI Agent core logic
│   │   │   ├── __init__.py
│   │   │   ├── core.py        # Main agent, analyzer, alert manager
│   │   │   ├── data_collector.py  # NAV data fetching
│   │   │   └── notifier.py    # Alert notifications
│   │   │
│   │   ├── api/               # FastAPI application
│   │   │   ├── __init__.py
│   │   │   ├── main.py        # Main API endpoints
│   │   │   └── health.py      # Health check endpoints
│   │   │
│   │   ├── backtest/          # Backtesting engine
│   │   │   ├── __init__.py
│   │   │   └── engine.py      # Strategy backtesting
│   │   │
│   │   ├── services/          # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── fund_service.py    # Fund CRUD operations
│   │   │   └── alert_service.py   # Alert management
│   │   │
│   │   ├── config.py          # Configuration management
│   │   └── database.py        # Database models and setup
│   │
│   ├── scripts/               # Utility scripts
│   │   └── find_fund.py       # Fund search utility
│   │
│   ├── tests/                 # Backend tests
│   │   ├── __init__.py
│   │   ├── test_agent.py
│   │   ├── test_api.py
│   │   └── test_backtest.py
│   │
│   ├── requirements.txt       # Python dependencies
│   ├── run_backend.py         # Backend launcher
│   └── .env.example           # Environment variables template
│
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.jsx      # Main dashboard
│   │   │   ├── FundManager.jsx    # Fund management
│   │   │   ├── BacktestPanel.jsx  # Backtesting UI
│   │   │   └── AlertsPanel.jsx    # Alerts display
│   │   │
│   │   ├── App.jsx            # Main app component
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Global styles
│   │
│   ├── public/                # Static assets
│   ├── index.html
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS config
│   └── postcss.config.js      # PostCSS config
│
├── docs/                      # Documentation
│   ├── AI_AGENT_DESIGN.md     # Architecture design
│   ├── API.md                 # API documentation
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── TROUBLESHOOTING.md     # Common issues
│
├── examples/                  # Example code
│   ├── example_usage.py       # Basic usage examples
│   └── backtest_example.py    # Backtesting examples
│
├── .github/                   # GitHub configuration
│   ├── workflows/             # CI/CD workflows
│   │   └── ci.yml
│   └── ISSUE_TEMPLATE/        # Issue templates
│
├── .gitignore                 # Git ignore rules
├── README.md                  # Main documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
└── PROJECT_STRUCTURE.md       # This file
```

## 🎯 Component Responsibilities

### Backend (`backend/`)

- **`src/agent/`**: Core AI agent logic for NAV monitoring
- **`src/api/`**: REST API endpoints and WebSocket handlers
- **`src/backtest/`**: Historical strategy testing
- **`src/services/`**: Database operations and business logic
- **`src/config.py`**: Configuration management
- **`src/database.py`**: SQLAlchemy models and database setup

### Frontend (`frontend/`)

- **`src/components/`**: Reusable React components
- **`src/App.jsx`**: Main application component
- **`src/main.jsx`**: Application entry point

### Documentation (`docs/`)

- Architecture designs
- API documentation
- Deployment guides
- Troubleshooting guides

### Examples (`examples/`)

- Code examples for common use cases
- Tutorial scripts

## 🔄 Data Flow

```
User (Browser)
    ↓
Frontend (React)
    ↓ HTTP/WebSocket
Backend API (FastAPI)
    ↓
AI Agent Core
    ↓
Data Collector → External APIs (MFAPI.in, AMFI)
    ↓
Database (SQLite/PostgreSQL)
```

## 📦 Dependencies

### Backend
- FastAPI - Web framework
- SQLAlchemy - ORM
- aiohttp - Async HTTP client
- pandas/numpy - Data analysis
- uvicorn - ASGI server

### Frontend
- React - UI library
- Vite - Build tool
- Tailwind CSS - Styling
- Recharts - Charts
- Lucide React - Icons

## 🗄️ Database Schema

- **funds**: Tracked mutual funds
- **alerts**: Generated alerts
- **nav_history**: Historical NAV data

## 🔧 Configuration

- Environment variables in `.env`
- Backend config in `src/config.py`
- Frontend config in `vite.config.js`

## 📝 Naming Conventions

- **Python**: snake_case for functions/variables, PascalCase for classes
- **JavaScript**: camelCase for variables/functions, PascalCase for components
- **Files**: lowercase with underscores (Python) or camelCase (JavaScript)

## 🚀 Entry Points

- **Backend**: `backend/run_backend.py`
- **Frontend**: `frontend/src/main.jsx`
- **Development**: See README.md for setup instructions

