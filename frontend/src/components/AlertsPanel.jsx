import React from 'react'
import { AlertTriangle, AlertCircle, Info, XCircle } from 'lucide-react'

export default function AlertsPanel({ alerts }) {
  const getSeverityIcon = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return <XCircle className="text-red-600" size={24} />
      case 'high':
        return <AlertTriangle className="text-orange-600" size={24} />
      case 'medium':
        return <AlertCircle className="text-yellow-600" size={24} />
      default:
        return <Info className="text-blue-600" size={24} />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'bg-red-50 border-red-200'
      case 'high':
        return 'bg-orange-50 border-orange-200'
      case 'medium':
        return 'bg-yellow-50 border-yellow-200'
      default:
        return 'bg-blue-50 border-blue-200'
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-6">Recent Alerts</h2>

      {alerts.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center">
          <AlertCircle className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-500 text-lg">No alerts yet</p>
          <p className="text-gray-400 text-sm mt-2">
            Alerts will appear here when NAV drops exceed your thresholds
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert, index) => (
            <div
              key={index}
              className={`bg-white rounded-xl p-6 shadow-lg border-2 ${getSeverityColor(alert.severity)}`}
            >
              <div className="flex items-start gap-4">
                <div className="mt-1">
                  {getSeverityIcon(alert.severity)}
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="text-lg font-bold text-gray-800">
                        {alert.fund?.scheme_name || 'Unknown Fund'}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {alert.fund?.scheme_code} • {alert.fund?.category}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      alert.severity === 'critical' ? 'bg-red-100 text-red-700' :
                      alert.severity === 'high' ? 'bg-orange-100 text-orange-700' :
                      alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {alert.severity.toUpperCase()}
                    </span>
                  </div>

                  <p className="text-gray-700 mb-4">{alert.message}</p>

                  <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
                    <div>
                      <div className="text-sm text-gray-500">Drop Percentage</div>
                      <div className="text-lg font-bold text-red-600">
                        {Math.abs(alert.drop_percentage).toFixed(2)}%
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Current NAV</div>
                      <div className="text-lg font-bold text-gray-800">
                        ₹{alert.current_nav.toFixed(2)}
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Previous NAV</div>
                      <div className="text-lg font-bold text-gray-800">
                        ₹{alert.previous_nav.toFixed(2)}
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 text-sm text-gray-500">
                    {new Date(alert.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

