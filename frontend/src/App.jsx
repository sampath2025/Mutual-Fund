import React, { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import FundManager from './components/FundManager'
import BacktestPanel from './components/BacktestPanel'
import AlertsPanel from './components/AlertsPanel'
import { TrendingUp, AlertCircle, BarChart3, Settings } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [funds, setFunds] = useState([])
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    fetchFunds()
    fetchAlerts()
    
    // Set up WebSocket connection for real-time updates
    let ws = null
    try {
      ws = new WebSocket(`ws://localhost:8000/ws`)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
      }
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'alert') {
            setAlerts(prev => [data, ...prev])
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }
      
      ws.onerror = (error) => {
        console.warn('WebSocket error (backend may not be ready):', error)
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
      }
    } catch (error) {
      console.warn('Failed to connect WebSocket (backend may not be ready):', error)
    }

    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [])

  const fetchFunds = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/funds`)
      const data = await response.json()
      setFunds(data)
    } catch (error) {
      console.error('Error fetching funds:', error)
    }
  }

  const fetchAlerts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/alerts?limit=20`)
      const data = await response.json()
      setAlerts(data)
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
    { id: 'funds', label: 'Manage Funds', icon: Settings },
    { id: 'backtest', label: 'Backtest', icon: BarChart3 },
    { id: 'alerts', label: 'Alerts', icon: AlertCircle },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Mutual Fund NAV Tracker
          </h1>
          <p className="text-blue-100">
            AI-Powered Monitoring & Alert System
          </p>
        </header>

        {/* Navigation Tabs */}
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-2 mb-6 flex gap-2">
          {tabs.map(tab => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-white text-indigo-700 shadow-lg'
                    : 'text-white hover:bg-white/20'
                }`}
              >
                <Icon size={20} />
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Main Content */}
        <div className="bg-white/10 backdrop-blur-lg rounded-xl shadow-2xl p-6">
          {activeTab === 'dashboard' && (
            <Dashboard funds={funds} onRefresh={fetchFunds} />
          )}
          {activeTab === 'funds' && (
            <FundManager funds={funds} onUpdate={fetchFunds} />
          )}
          {activeTab === 'backtest' && (
            <BacktestPanel />
          )}
          {activeTab === 'alerts' && (
            <AlertsPanel alerts={alerts} />
          )}
        </div>
      </div>
    </div>
  )
}

export default App

