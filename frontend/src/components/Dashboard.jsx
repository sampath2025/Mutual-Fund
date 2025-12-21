import React, { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { TrendingUp, TrendingDown, DollarSign, AlertTriangle } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Dashboard({ funds, onRefresh }) {
  const [navData, setNavData] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadNavData()
    const interval = setInterval(loadNavData, 60000) // Refresh every minute
    return () => clearInterval(interval)
  }, [funds])

  const loadNavData = async () => {
    setLoading(true)
    const data = {}
    for (const fund of funds) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/nav/${fund.scheme_code}?days=30`)
        const navInfo = await response.json()
        data[fund.scheme_code] = navInfo
      } catch (error) {
        console.error(`Error loading NAV for ${fund.scheme_name}:`, error)
      }
    }
    setNavData(data)
    setLoading(false)
  }

  const getChartData = (schemeCode) => {
    const fundData = navData[schemeCode]
    if (!fundData || !fundData.historical_nav) return []
    
    return fundData.historical_nav
      .slice()
      .reverse()
      .map(item => ({
        date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        nav: parseFloat(item.nav)
      }))
  }

  const calculateChange = (schemeCode) => {
    const fundData = navData[schemeCode]
    if (!fundData || !fundData.historical_nav || fundData.historical_nav.length < 2) {
      return { percentage: 0, value: 0 }
    }
    
    const latest = fundData.historical_nav[0].nav
    const previous = fundData.historical_nav[1].nav
    const change = ((latest - previous) / previous) * 100
    
    return {
      percentage: change,
      value: latest - previous
    }
  }

  if (loading && Object.keys(navData).length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-white text-lg">Loading fund data...</div>
      </div>
    )
  }

  if (funds.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-white text-lg mb-4">No funds tracked yet</p>
        <p className="text-blue-100">Add funds from the "Manage Funds" tab to get started</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Fund Performance Dashboard</h2>
        <button
          onClick={loadNavData}
          className="px-4 py-2 bg-white text-indigo-700 rounded-lg font-medium hover:bg-blue-50 transition"
        >
          Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {funds.map(fund => {
          const change = calculateChange(fund.scheme_code)
          const fundData = navData[fund.scheme_code]
          const currentNav = fundData?.latest_nav?.nav || 0
          const isPositive = change.percentage >= 0

          return (
            <div
              key={fund.scheme_code}
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-gray-800 text-lg">{fund.scheme_name}</h3>
                  <p className="text-sm text-gray-500">{fund.category}</p>
                </div>
                {isPositive ? (
                  <TrendingUp className="text-green-500" size={24} />
                ) : (
                  <TrendingDown className="text-red-500" size={24} />
                )}
              </div>

              <div className="mb-4">
                <div className="flex items-baseline gap-2">
                  <DollarSign size={20} className="text-gray-400" />
                  <span className="text-3xl font-bold text-gray-800">
                    ₹{currentNav.toFixed(2)}
                  </span>
                </div>
                <div className={`flex items-center gap-1 mt-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                  {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                  <span className="font-semibold">
                    {Math.abs(change.percentage).toFixed(2)}%
                  </span>
                  <span className="text-sm text-gray-500">
                    ({isPositive ? '+' : ''}₹{change.value.toFixed(2)})
                  </span>
                </div>
              </div>

              <div className="h-32">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={getChartData(fund.scheme_code)}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis dataKey="date" stroke="#666" fontSize={10} />
                    <YAxis stroke="#666" fontSize={10} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        border: '1px solid #e0e0e0',
                        borderRadius: '8px'
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="nav"
                      stroke={isPositive ? "#10b981" : "#ef4444"}
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Alert Threshold</span>
                  <span className="font-semibold text-gray-700">{fund.alert_threshold}%</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

