import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { Sparkles, Settings, Eye, EyeOff } from 'lucide-react'

const LLMNode = ({ data, isConnectable }) => {
  const [showConfig, setShowConfig] = useState(false)
  const [showApiKey, setShowApiKey] = useState(false)
  const [config, setConfig] = useState({
    model: data.model || 'gemini-flash-latest',
    apiKey: data.apiKey || '',
    prompt: data.prompt || 'You are a helpful PDF assistant. Use web search if the PDF lacks context\n\nCONTEXT: {context}\nUser Query: {query}',
    temperature: data.temperature || 0.75,
    useWebSearch: data.useWebSearch || false,
    serpApiKey: data.serpApiKey || ''
  })

  const handleChange = (field, value) => {
    const newConfig = { ...config, [field]: value }
    setConfig(newConfig)
    data.onChange?.(newConfig)
  }

  return (
    <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200 min-w-[300px] max-w-[350px]">
      <div className="flex items-center justify-between p-3 border-b bg-gray-50">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-purple-600" />
          <span className="font-medium text-sm">LLM (Gemini)</span>
        </div>
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="p-1 hover:bg-gray-200 rounded transition-colors"
        >
          <Settings className="w-4 h-4" />
        </button>
      </div>
      
      <div className="p-3">
        <p className="text-xs text-gray-600 mb-2">Run a query with Gemini LLM</p>
        
        {showConfig && (
          <div className="mt-2 space-y-3 max-h-96 overflow-y-auto">
            <div>
              <label className="block text-xs text-gray-700 mb-1">Model</label>
              <select
                className="w-full px-2 py-1 text-sm border rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
                value={config.model}
                onChange={(e) => handleChange('model', e.target.value)}
              >
                <option value="gemini-flash-latest">Gemini Flash</option>
                <option value="gemini-pro">Gemini Pro</option>
              </select>
            </div>
            
            <div>
              <label className="block text-xs text-gray-700 mb-1">API Key</label>
              <div className="relative">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  className="w-full px-2 py-1 pr-8 text-sm border rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="Enter Gemini API key"
                  value={config.apiKey}
                  onChange={(e) => handleChange('apiKey', e.target.value)}
                />
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="absolute right-2 top-1/2 -translate-y-1/2"
                >
                  {showApiKey ? (
                    <EyeOff className="w-4 h-4 text-gray-400" />
                  ) : (
                    <Eye className="w-4 h-4 text-gray-400" />
                  )}
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-xs text-gray-700 mb-1">Prompt</label>
              <textarea
                className="w-full px-2 py-1 text-xs border rounded focus:outline-none focus:ring-1 focus:ring-primary-500 font-mono"
                rows={4}
                value={config.prompt}
                onChange={(e) => handleChange('prompt', e.target.value)}
              />
              <p className="text-xs text-gray-500 mt-1">
                Use <span className="font-mono bg-gray-100 px-1">{'{context}'}</span> and{' '}
                <span className="font-mono bg-gray-100 px-1">{'{query}'}</span>
              </p>
            </div>
            
            <div>
              <label className="block text-xs text-gray-700 mb-1">
                Temperature: {config.temperature}
              </label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.1"
                className="w-full"
                value={config.temperature}
                onChange={(e) => handleChange('temperature', parseFloat(e.target.value))}
              />
            </div>
            
            <div className="flex items-center justify-between">
              <label className="text-xs text-gray-700">WebSearch Tool</label>
              <button
                type="button"
                onClick={() => handleChange('useWebSearch', !config.useWebSearch)}
                className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                  config.useWebSearch ? 'bg-primary-600' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    config.useWebSearch ? 'translate-x-5' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
            
            {config.useWebSearch && (
              <div>
                <label className="block text-xs text-gray-700 mb-1">SERF API</label>
                <input
                  type="password"
                  className="w-full px-2 py-1 text-sm border rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="Enter SerpAPI key"
                  value={config.serpApiKey}
                  onChange={(e) => handleChange('serpApiKey', e.target.value)}
                />
              </div>
            )}
          </div>
        )}
      </div>
      
      <Handle
        type="target"
        position={Position.Left}
        id="query"
        style={{ background: '#f59e0b', top: '35%' }}
        isConnectable={isConnectable}
      />
      <Handle
        type="target"
        position={Position.Left}
        id="context"
        style={{ background: '#ef4444', top: '65%' }}
        isConnectable={isConnectable}
      />
      <Handle
        type="source"
        position={Position.Right}
        id="output"
        style={{ background: '#10b981' }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default LLMNode