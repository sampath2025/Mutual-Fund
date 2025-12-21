# Mutual Fund NAV Tracker - Frontend

## 🎨 Tech Stack

Pure React stack with modern tools:

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Recharts** - Chart library
- **Lucide React** - Icon library
- **WebSocket** - Real-time updates

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx      # Main dashboard with charts
│   │   ├── FundManager.jsx   # Fund management
│   │   ├── BacktestPanel.jsx # Backtesting interface
│   │   └── AlertsPanel.jsx   # Alerts display
│   ├── App.jsx               # Main app component
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### API Connection

The frontend connects to the backend API at:
- REST API: `http://localhost:8000/api`
- WebSocket: `ws://localhost:8000/ws`

## 🎯 Features

- **Real-time NAV Updates** - WebSocket connection for live data
- **Interactive Charts** - 30-day NAV trends with Recharts
- **Responsive Design** - Works on all devices
- **Modern UI** - Beautiful gradient theme with Tailwind CSS

## 🐛 Troubleshooting

### Import Errors
- Make sure all dependencies are installed: `npm install`
- Clear cache: `rm -rf node_modules && npm install`

### WebSocket Errors
- Ensure backend is running on port 8000
- WebSocket errors are handled gracefully (app still works)

### Build Errors
- Check Node.js version (18+)
- Clear Vite cache: `rm -rf node_modules/.vite`

## 📦 Dependencies

### Production
- `react` - UI library
- `react-dom` - React DOM bindings
- `recharts` - Chart components
- `lucide-react` - Icons

### Development
- `vite` - Build tool
- `@vitejs/plugin-react` - React plugin for Vite
- `tailwindcss` - CSS framework
- `autoprefixer` - CSS post-processor

## 🎨 Styling

Uses Tailwind CSS for all styling:
- Utility-first CSS
- Responsive design
- Custom gradient theme
- Dark/light mode ready

## 🔄 Real-time Updates

WebSocket connection provides:
- Live NAV updates
- Instant alert notifications
- Real-time dashboard refresh

---

**Built with React + Vite + Tailwind CSS** ⚡

