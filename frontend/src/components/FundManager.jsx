import React, { useState } from 'react'
import { Plus, Trash2, Search, ExternalLink } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function FundManager({ funds, onUpdate }) {
  const [showAddForm, setShowAddForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [fundSearchQuery, setFundSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [searching, setSearching] = useState(false)
  const [formData, setFormData] = useState({
    scheme_code: '',
    scheme_name: '',
    fund_house: '',
    category: '',
    alert_threshold: 2.0
  })

  const handleAddFund = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE_URL}/api/funds`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        const newFund = await response.json()
        onUpdate()
        setShowAddForm(false)
        setFormData({
          scheme_code: '',
          scheme_name: '',
          fund_house: '',
          category: '',
          alert_threshold: 2.0
        })
        alert('Fund added successfully!')
      } else {
        const error = await response.json()
        alert(`Error: ${error.detail || 'Failed to add fund'}`)
      }
    } catch (error) {
      alert(`Error: ${error.message}`)
    }
  }

  const handleDeleteFund = async (schemeCode) => {
    if (!confirm('Are you sure you want to remove this fund from tracking?')) {
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/funds/${schemeCode}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        onUpdate()
        alert('Fund removed successfully!')
      } else {
        alert('Failed to remove fund')
      }
    } catch (error) {
      alert(`Error: ${error.message}`)
    }
  }

  const filteredFunds = funds.filter(fund =>
    fund.scheme_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    fund.scheme_code.includes(searchQuery)
  )

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Manage Tracked Funds</h2>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center gap-2 px-4 py-2 bg-white text-indigo-700 rounded-lg font-medium hover:bg-blue-50 transition"
        >
          <Plus size={20} />
          Add Fund
        </button>
      </div>

      {showAddForm && (
        <div className="bg-white rounded-xl p-6 mb-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Add New Fund</h3>
          <form onSubmit={handleAddFund} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scheme Code *
                </label>
                <input
                  type="text"
                  required
                  value={formData.scheme_code}
                  onChange={(e) => setFormData({ ...formData, scheme_code: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="e.g., 125497"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scheme Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.scheme_name}
                  onChange={(e) => setFormData({ ...formData, scheme_name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="e.g., HDFC Equity Fund"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fund House *
                </label>
                <input
                  type="text"
                  required
                  value={formData.fund_house}
                  onChange={(e) => setFormData({ ...formData, fund_house: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="e.g., HDFC Mutual Fund"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category *
                </label>
                <input
                  type="text"
                  required
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="e.g., Equity, Debt, Hybrid"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Alert Threshold (%) *
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0.1"
                  max="20"
                  required
                  value={formData.alert_threshold}
                  onChange={(e) => setFormData({ ...formData, alert_threshold: parseFloat(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex gap-3">
              <button
                type="submit"
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition"
              >
                Add Fund
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="mb-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <h4 className="font-semibold text-blue-800 mb-2">Can't find your fund?</h4>
          <p className="text-sm text-blue-700 mb-3">
            Search for funds by name to find the correct scheme code, or find it manually:
          </p>
          <div className="flex gap-2">
              <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search fund name (e.g., Nippon Realty)..."
                value={fundSearchQuery}
                onChange={(e) => setFundSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearchFunds()}
                className="w-full pl-10 pr-4 py-2 bg-white rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={handleSearchFunds}
              disabled={searching}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition disabled:opacity-50"
            >
              {searching ? 'Searching...' : 'Search'}
            </button>
            <a
              href="https://www.mfapi.in/"
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition flex items-center gap-2"
            >
              <ExternalLink size={16} />
              MFAPI.in
            </a>
          </div>
        </div>

        {searchResults.length > 0 && (
          <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4 max-h-64 overflow-y-auto">
            <h4 className="font-semibold text-gray-800 mb-2">Search Results:</h4>
            <div className="space-y-2">
              {searchResults.map((result, index) => (
                <div
                  key={index}
                  className="p-3 border border-gray-200 rounded-lg hover:bg-blue-50 cursor-pointer transition"
                  onClick={() => handleSelectSearchResult(result)}
                >
                  <div className="font-semibold text-gray-800">{result.scheme_name}</div>
                  <div className="text-sm text-gray-600">
                    Code: {result.scheme_code} | {result.fund_house || 'N/A'}
                    {result.nav && ` | NAV: ₹${result.nav.toFixed(2)}`}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Filter tracked funds..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>
      </div>

      <div className="space-y-4">
        {filteredFunds.length === 0 ? (
          <div className="bg-white rounded-xl p-8 text-center">
            <p className="text-gray-500">No funds found. Add your first fund to get started!</p>
          </div>
        ) : (
          filteredFunds.map(fund => (
            <div
              key={fund.scheme_code}
              className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-800 mb-1">{fund.scheme_name}</h3>
                  <div className="grid grid-cols-2 gap-4 mt-3 text-sm">
                    <div>
                      <span className="text-gray-500">Scheme Code:</span>
                      <span className="ml-2 font-semibold text-gray-700">{fund.scheme_code}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Fund House:</span>
                      <span className="ml-2 font-semibold text-gray-700">{fund.fund_house}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Category:</span>
                      <span className="ml-2 font-semibold text-gray-700">{fund.category}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Alert Threshold:</span>
                      <span className="ml-2 font-semibold text-indigo-600">{fund.alert_threshold}%</span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteFund(fund.scheme_code)}
                  className="ml-4 p-2 text-red-500 hover:bg-red-50 rounded-lg transition"
                  title="Remove fund"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

