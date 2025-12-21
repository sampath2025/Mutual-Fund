# Backend - Mutual Fund NAV Tracker

Python FastAPI backend for the Mutual Fund NAV Tracker application.

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run server
python run_backend.py
```

## 📁 Structure

- `src/agent/` - AI agent core logic
- `src/api/` - FastAPI endpoints
- `src/backtest/` - Backtesting engine
- `src/services/` - Business logic services
- `src/config.py` - Configuration
- `src/database.py` - Database models

## 🔧 Configuration

See `.env.example` for all configuration options.

## 📚 API Documentation

Once running, visit: http://localhost:8000/docs

## 🧪 Testing

```bash
pytest tests/
```

## 📝 More Info

See main [README.md](../README.md) for complete documentation.

