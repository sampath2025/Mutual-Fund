# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run backend server
python run_backend.py
```

Backend will run on: http://localhost:8000

### Step 2: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend will run on: http://localhost:3000

### Step 3: Add Your First Fund

1. Open http://localhost:3000 in your browser
2. Click "Manage Funds" tab
3. Click "Add Fund"
4. Enter:
   - **Scheme Code**: `125497` (HDFC Equity Fund - example)
   - **Scheme Name**: `HDFC Equity Fund`
   - **Fund House**: `HDFC Mutual Fund`
   - **Category**: `Equity`
   - **Alert Threshold**: `2.0` (2% drop will trigger alert)

5. Click "Add Fund"

### Step 4: View Dashboard

1. Go to "Dashboard" tab
2. See real-time NAV updates
3. View 30-day historical charts

### Step 5: Test Backtesting

1. Go to "Backtest" tab
2. Enter scheme code: `125497`
3. Set threshold: `2.0`
4. Click "Run Backtest"
5. View performance metrics

## 📊 Finding Scheme Codes

### Method 1: AMFI Website
1. Visit: https://www.amfiindia.com/
2. Navigate to NAV data
3. Find your fund's scheme code

### Method 2: MFAPI.in
1. Visit: https://www.mfapi.in/
2. Search for your fund
3. Get the scheme code from URL

### Popular Scheme Codes (Examples)
- HDFC Equity Fund: `125497`
- SBI Bluechip Fund: `120465`
- ICICI Prudential Technology Fund: `120465`

## 🔔 Setting Up Email Alerts

Edit `src/agent/notifier.py`:

```python
email_config = {
    'enabled': True,
    'sender_email': 'your-email@gmail.com',
    'receiver_email': 'recipient@example.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'password': 'your-app-password'  # Use App Password for Gmail
}
```

For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in the config

## 🧪 Testing the System

### Test with Example Script

```bash
python examples/example_usage.py
```

### Test Backtesting

```bash
python examples/backtest_example.py
```

## 📱 API Endpoints

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

### Key Endpoints:
- `GET /api/funds` - List all funds
- `POST /api/funds` - Add a fund
- `GET /api/nav/{scheme_code}` - Get NAV data
- `POST /api/backtest` - Run backtest
- `WebSocket /ws` - Real-time updates

## 🎯 Next Steps

1. Add multiple funds to track
2. Customize alert thresholds
3. Run backtests to optimize thresholds
4. Set up email notifications
5. Monitor your dashboard regularly

## ❓ Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Ensure all dependencies are installed
- Check Python version (3.9+)

### Frontend won't start
- Check if port 3000 is available
- Run `npm install` again
- Clear `node_modules` and reinstall

### No NAV data
- Verify scheme code is correct
- Check internet connection
- API might be temporarily unavailable

### Alerts not working
- Check alert threshold settings
- Verify fund is active
- Check notification configuration

## 📚 Learn More

- Read `docs/AI_AGENT_DESIGN.md` for architecture details
- Check `README.md` for full documentation
- Explore API docs at `/docs` endpoint

---

**Happy Tracking! 📈**

