# Mutual Fund NAV Tracker - AI-Powered Alert System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

A comprehensive web application for tracking Mutual Fund NAVs with intelligent alerting and backtesting capabilities.

## 🎯 Features

- **AI-Powered Monitoring**: Intelligent NAV tracking with pattern recognition and anomaly detection
- **Real-time Alerts**: Multi-threshold alert system with email notifications
- **Backtesting Engine**: Test your alert strategies on historical data
- **Modern UI**: Beautiful, responsive dashboard built with React
- **Free API Integration**: Uses AMFI and MFAPI.in for real-time NAV data
- **Database Persistence**: SQLite/PostgreSQL support for data storage

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │
│  (Dashboard UI) │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI Backend│
│  (REST + WebSocket)
└────────┬────────┘
         │
┌────────▼────────┐
│  AI Agent Core   │
│  - Data Collector│
│  - Analyzer      │
│  - Alert Manager │
│  - Backtest Engine│
└──────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sumanth2525/Mutual-Fund.git
cd Mutual-Fund
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run the API server
python run_backend.py
```

Backend will run on: **http://localhost:8000**

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

### 4. Access the Application

- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000

## 📖 Usage Guide

### Adding Funds

1. Navigate to "Manage Funds" tab
2. Click "Add Fund"
3. Enter:
   - Scheme Code (e.g., 125497 for HDFC Equity Fund)
   - Scheme Name
   - Fund House
   - Category
   - Alert Threshold (default: 2%)

### Monitoring

- Dashboard shows real-time NAV updates
- Charts display 30-day historical trends
- Color-coded indicators show performance

### Backtesting

1. Go to "Backtest" tab
2. Enter scheme code and threshold
3. Click "Run Backtest" to see strategy performance
4. Use "Find Optimal Threshold" to optimize your alerts

### Alerts

- Alerts appear automatically when NAV drops exceed thresholds
- View all alerts in the "Alerts" tab
- Alerts are categorized by severity (Low, Medium, High, Critical)

## 📁 Project Structure

```
Mutual-Fund/
├── backend/          # Python FastAPI backend
├── frontend/         # React frontend
├── docs/            # Documentation
├── examples/        # Example code
└── README.md        # This file
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

## 🔧 Configuration

### Environment Variables

See `backend/.env.example` for all configuration options.

### Key Settings

- `DATABASE_URL`: Database connection string
- `AGENT_CHECK_INTERVAL`: How often to check NAVs (seconds)
- `EMAIL_ENABLED`: Enable email notifications
- `CORS_ORIGINS`: Allowed CORS origins

## 📊 API Endpoints

- `GET /api/funds` - List all tracked funds
- `POST /api/funds` - Add a new fund
- `DELETE /api/funds/{code}` - Remove a fund
- `GET /api/nav/{code}` - Get NAV data
- `GET /api/alerts` - Get recent alerts
- `POST /api/backtest` - Run backtest
- `POST /api/backtest/optimize` - Find optimal threshold
- `GET /api/search?query=...` - Search for funds
- `WebSocket /ws` - Real-time updates

Full API documentation: http://localhost:8000/docs

## 🧪 Testing

### Backend

```bash
cd backend
pytest tests/
```

### Frontend

```bash
cd frontend
npm test
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Documentation

- [Project Structure](PROJECT_STRUCTURE.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Backend Setup](docs/BACKEND_SETUP.md)
- [API Documentation](docs/API.md) (coming soon)
- [Deployment Guide](docs/DEPLOYMENT.md) (coming soon)

## 🔍 Finding Scheme Codes

You can find scheme codes from:
- AMFI website: https://www.amfiindia.com/
- MFAPI.in: https://www.mfapi.in/
- Use the search feature in the web app
- Fund house websites

## 🚧 Roadmap

- [ ] User authentication and multi-user support
- [ ] SMS notifications
- [ ] Mobile app (React Native)
- [ ] Portfolio tracking and analytics
- [ ] Comparison with market indices
- [ ] Machine learning-based predictions
- [ ] Export reports (PDF/Excel)
- [ ] Scheduled email reports

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for informational purposes only. It does not provide investment advice. Always consult with a financial advisor before making investment decisions.

## 👥 Contributors

- [Your Name](https://github.com/yourusername)

## 📞 Support

For issues or questions:
- Open an issue on [GitHub Issues](https://github.com/sumanth2525/Mutual-Fund/issues)
- Check the [documentation](docs/)
- Review [troubleshooting guide](docs/TROUBLESHOOTING.md)

---

**Built with ❤️ for smart investors**
