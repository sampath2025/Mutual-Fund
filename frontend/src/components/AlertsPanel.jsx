import React, { useState, useEffect } from 'react'
import { AlertTriangle, AlertCircle, Info, XCircle, Mail, Save, Loader2 } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function AlertsPanel({ alerts }) {
  const [showConfig, setShowConfig] = useState(false)
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState(null)
  
  const [emailConfig, setEmailConfig] = useState({
    enabled: false,
    sender_email: '',
    receiver_email: '',
    password: '',
    smtp_server: 'smtp.gmail.com',
    smtp_port: 587
  })

  useEffect(() => {
    if (showConfig) {
      fetchEmailConfig()
    }
  }, [showConfig])

  const fetchEmailConfig = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/settings/email`)
      const data = await response.json()
      if (data && Object.keys(data).length > 0) {
        setEmailConfig(prev => ({ ...prev, ...data }))
      }
    } catch (error) {
      console.error('Error fetching email config:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveConfig = async (e) => {
    e.preventDefault()
    setSaving(true)
    setMessage(null)
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/settings/email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(emailConfig)
      })
      
      if (response.ok) {
        setMessage({ type: 'success', text: 'Settings saved successfully' })
      } else {
        setMessage({ type: 'error', text: 'Failed to save settings' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error saving settings: ' + error.message })
    } finally {
      setSaving(false)
    }
  }

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
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Alerts System</h2>
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors backdrop-blur-sm"
        >
          <Mail size={20} />
          {showConfig ? 'View Alerts' : 'Configure Email'}
        </button>
      </div>

      {showConfig ? (
        <div className="bg-white rounded-xl p-6 shadow-xl">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Email Notification Settings</h3>
          <div className="bg-blue-50 p-4 rounded-lg mb-6 text-sm text-blue-700">
            <p className="font-semibold mb-1">Note for Gmail Users:</p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Use your full Gmail address as Sender Email</li>
              <li>You must use an <strong>App Password</strong> instead of your regular password</li>
              <li>Enable 2-Step Verification in Google Account {'>'} Security to generate an App Password</li>
            </ul>
          </div>
          
          {loading ? (
            <div className="flex justify-center p-8">
              <Loader2 className="animate-spin text-indigo-600" size={32} />
            </div>
          ) : (
            <form onSubmit={handleSaveConfig} className="space-y-4 max-w-2xl">
              <div className="flex items-center gap-2 mb-4">
                <input
                  type="checkbox"
                  id="enabled"
                  checked={emailConfig.enabled}
                  onChange={e => setEmailConfig({...emailConfig, enabled: e.target.checked})}
                  className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                />
                <label htmlFor="enabled" className="font-medium text-gray-700">Enable Email Notifications</label>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Sender Email</label>
                  <input
                    type="email"
                    value={emailConfig.sender_email || ''}
                    onChange={e => setEmailConfig({...emailConfig, sender_email: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                    placeholder="your-email@gmail.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">App Password</label>
                  <input
                    type="password"
                    value={emailConfig.password || ''}
                    onChange={e => setEmailConfig({...emailConfig, password: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                    placeholder="xxxx xxxx xxxx xxxx"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Receiver Email</label>
                  <input
                    type="email"
                    value={emailConfig.receiver_email || ''}
                    onChange={e => setEmailConfig({...emailConfig, receiver_email: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                    placeholder="recipient@example.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">SMTP Server</label>
                  <input
                    type="text"
                    value={emailConfig.smtp_server}
                    onChange={e => setEmailConfig({...emailConfig, smtp_server: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                  />
                </div>
              </div>

              {message && (
                <div className={`p-3 rounded-lg text-sm ${
                  message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                }`}>
                  {message.text}
                </div>
              )}

              <div className="pt-4">
                <button
                  type="submit"
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50"
                >
                  {saving ? <Loader2 className="animate-spin" size={20} /> : <Save size={20} />}
                  Save Settings
                </button>
              </div>
            </form>
          )}
        </div>
      ) : (
        alerts.length === 0 ? (
          <div className="bg-white rounded-xl p-12 text-center shadow-xl">
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
                className={`bg-white rounded-xl p-6 shadow-lg border-2 ${getSeverityColor(alert.severity)} transition-transform hover:scale-[1.01]`}
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
        )
      )}
    </div>
  )
}

