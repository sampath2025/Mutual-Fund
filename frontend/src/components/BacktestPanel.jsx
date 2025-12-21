import React, { useState } from 'react'
import { Play, TrendingUp, TrendingDown, BarChart3, Target } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function BacktestPanel() {
  const [schemeCode, setSchemeCode] = useState('')
  const [threshold, setThreshold] = useState(2.0)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [optimizationResults, setOptimizationResults] = useState(null)

  const runBacktest = async () => {
    if (!schemeCode) {
      alert('Please enter a scheme code')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/backtest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scheme_code: schemeCode,
          threshold: threshold,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setResults(data.results)
      } else {
        const error = await response.json()
        alert(`Error: ${error.detail || 'Backtest failed'}`)
      }
    } catch (error) {
      alert(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const optimizeThreshold = async () => {
    if (!schemeCode) {
      alert('Please enter a scheme code')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/backtest/optimize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scheme_code: schemeCode,
          threshold: threshold,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setOptimizationResults(data)
        setThreshold(data.optimal_threshold)
      } else {
        const error = await response.json()
        alert(`Error: ${error.detail || 'Optimization failed'}`)
      }
    } catch (error) {
      alert(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Strategy Backtesting</h2>

      <div className="bg-white rounded-xl p-6 shadow-lg mb-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Backtest Configuration</h3>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Scheme Code *
            </label>
            <input
              type="text"
              value={schemeCode}
              onChange={(e) => setSchemeCode(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="e.g., 125497"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Drop Threshold (%) *
            </label>
            <input
              type="number"
              step="0.1"
              min="0.1"
              max="20"
              value={threshold}
              onChange={(e) => setThreshold(parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
        </div>
        <div className="flex gap-3">
          <button
            onClick={runBacktest}
            disabled={loading}
            className="flex items-center gap-2 px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition disabled:opacity-50"
          >
            <Play size={20} />
            Run Backtest
          </button>
          <button
            onClick={optimizeThreshold}
            disabled={loading}
            className="flex items-center gap-2 px-6 py-2 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition disabled:opacity-50"
          >
            <Target size={20} />
            Find Optimal Threshold
          </button>
        </div>
      </div>

      {optimizationResults && (
        <div className="bg-white rounded-xl p-6 shadow-lg mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Optimization Results</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-indigo-50 rounded-lg p-4">
              <div className="text-sm text-gray-600">Optimal Threshold</div>
              <div className="text-2xl font-bold text-indigo-600">
                {optimizationResults.optimal_threshold}%
              </div>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-sm text-gray-600">Best F1 Score</div>
              <div className="text-2xl font-bold text-green-600">
                {optimizationResults.best_f1_score}%
              </div>
            </div>
          </div>
        </div>
      )}

      {results && (
        <div className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="text-blue-500" size={24} />
                <span className="text-sm text-gray-600">Accuracy</span>
              </div>
              <div className="text-3xl font-bold text-gray-800">{results.accuracy}%</div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="text-green-500" size={24} />
                <span className="text-sm text-gray-600">Precision</span>
              </div>
              <div className="text-3xl font-bold text-gray-800">{results.precision}%</div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <Target className="text-purple-500" size={24} />
                <span className="text-sm text-gray-600">Recall</span>
              </div>
              <div className="text-3xl font-bold text-gray-800">{results.recall}%</div>
            </div>
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="text-orange-500" size={24} />
                <span className="text-sm text-gray-600">F1 Score</span>
              </div>
              <div className="text-3xl font-bold text-gray-800">{results.f1_score}%</div>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Detailed Results</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-600">Total Alerts</div>
                <div className="text-2xl font-bold text-gray-800">{results.total_alerts}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">True Positives</div>
                <div className="text-2xl font-bold text-green-600">{results.true_positives}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">False Positives</div>
                <div className="text-2xl font-bold text-red-600">{results.false_positives}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Avg Drop After Alert</div>
                <div className="text-2xl font-bold text-gray-800">{results.avg_drop_after_alert}%</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Max Drop After Alert</div>
                <div className="text-2xl font-bold text-red-600">{results.max_drop_after_alert}%</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Avg Recovery Time</div>
                <div className="text-2xl font-bold text-gray-800">
                  {results.avg_recovery_time ? `${results.avg_recovery_time} days` : 'N/A'}
                </div>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Performance Metrics</h3>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-600">Sharpe Ratio</div>
                <div className="text-xl font-bold text-gray-800">
                  {results.performance_metrics.sharpe_ratio}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Max Drawdown</div>
                <div className="text-xl font-bold text-red-600">
                  {results.performance_metrics.max_drawdown}%
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Volatility</div>
                <div className="text-xl font-bold text-gray-800">
                  {results.performance_metrics.volatility}%
                </div>
              </div>
            </div>
          </div>

          {/* Alerts by Severity */}
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Alerts by Severity</h3>
            <div className="grid grid-cols-4 gap-4">
              {Object.entries(results.alerts_by_severity).map(([severity, count]) => (
                <div key={severity} className="text-center">
                  <div className="text-2xl font-bold text-gray-800">{count}</div>
                  <div className="text-sm text-gray-600 capitalize">{severity}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="text-center py-8">
          <div className="text-white text-lg">Running backtest...</div>
        </div>
      )}
    </div>
  )
}

