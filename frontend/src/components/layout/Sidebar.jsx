import React from 'react'
import { Minimize2 } from 'lucide-react'

const Sidebar = ({ title, children, onMinimize }) => {
  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">{title}</h3>
        {onMinimize && (
          <button
            onClick={onMinimize}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        {children}
      </div>
    </div>
  )
}

export default Sidebar