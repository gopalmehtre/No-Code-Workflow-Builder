import React from 'react'
import { Handle, Position } from 'reactflow'
import { ArrowRight, Settings } from 'lucide-react'

const OutputNode = ({ data, isConnectable }) => {
  return (
    <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200 min-w-[250px]">
      <div className="flex items-center justify-between p-3 border-b bg-gray-50">
        <div className="flex items-center gap-2">
          <ArrowRight className="w-4 h-4 text-gray-600" />
          <span className="font-medium text-sm">Output</span>
        </div>
        <Settings className="w-4 h-4 text-gray-400" />
      </div>
      
      <div className="p-3">
        <p className="text-xs text-gray-600 mb-2">Output of the result nodes as text</p>
        
        <div className="mt-2">
          <label className="block text-xs text-gray-700 mb-1">Output Text</label>
          <div className="p-2 bg-gray-50 border border-gray-200 rounded text-xs text-gray-500">
            Output will be generated based on query
          </div>
        </div>
      </div>
      
      <Handle
        type="target"
        position={Position.Left}
        id="output"
        style={{ background: '#10b981' }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default OutputNode