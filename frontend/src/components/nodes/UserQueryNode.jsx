import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { MessageSquare, Settings } from 'lucide-react'

const UserQueryNode = ({ data, isConnectable }) => {
  const [showConfig, setShowConfig] = useState(false)
  
  return (
    <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200 min-w-[250px]">
      <div className="flex items-center justify-between p-3 border-b bg-gray-50">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-gray-600" />
          <span className="font-medium text-sm">User Query</span>
        </div>
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="p-1 hover:bg-gray-200 rounded transition-colors"
        >
          <Settings className="w-4 h-4" />
        </button>
      </div>
      
      <div className="p-3">
        <p className="text-xs text-gray-600 mb-2">Enter point for querys</p>
        
        {showConfig && (
          <div className="mt-2">
            <label className="block text-xs text-gray-700 mb-1">User Query</label>
            <input
              type="text"
              placeholder="Write your query here"
              className="w-full px-2 py-1 text-sm border rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
              value={data.query || ''}
              onChange={(e) => data.onChange?.({ query: e.target.value })}
            />
          </div>
        )}
      </div>
      
      <Handle
        type="source"
        position={Position.Right}
        id="query"
        style={{ background: '#f59e0b' }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default UserQueryNode