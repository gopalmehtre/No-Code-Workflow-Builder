import React, { useState } from 'react'
import { MessageSquare, Book, Sparkles, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react'

const components = [
  {
    type: 'user_query',
    label: 'User Query',
    icon: MessageSquare,
    description: 'Entry point for user input'
  },
  {
    type: 'knowledge_base',
    label: 'Knowledge Base',
    icon: Book,
    description: 'Upload and search documents'
  },
  {
    type: 'llm_engine',
    label: 'LLM (Gemini)',
    icon: Sparkles,
    description: 'AI language model'
  },
  {
    type: 'output',
    label: 'Output',
    icon: ArrowRight,
    description: 'Display results'
  }
]

const ComponentSidebar = ({ workflowName }) => {
  const [isCollapsed, setIsCollapsed] = useState(false)

  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }

  if (isCollapsed) {
    return (
      <div className="w-12 bg-white border-r border-gray-200 flex flex-col items-center py-4">
        <button
          onClick={() => setIsCollapsed(false)}
          className="p-2 hover:bg-gray-100 rounded transition-colors"
        >
          <ChevronRight className="w-5 h-5 text-gray-600" />
        </button>
      </div>
    )
  }

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <div className="flex-1">
          <h2 className="font-semibold text-gray-900 truncate">{workflowName}</h2>
        </div>
        <button
          onClick={() => setIsCollapsed(true)}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
        >
          <ChevronLeft className="w-5 h-5 text-gray-600" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Components</h3>
        <div className="space-y-2">
          {components.map((component) => {
            const Icon = component.icon
            return (
              <div
                key={component.type}
                draggable
                onDragStart={(e) => onDragStart(e, component.type)}
                className="flex items-center gap-3 p-3 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg cursor-move transition-colors group"
              >
                <Icon className="w-5 h-5 text-gray-600 group-hover:text-primary-600" />
                <div className="flex-1">
                  <div className="font-medium text-sm text-gray-900">{component.label}</div>
                  <div className="text-xs text-gray-500">{component.description}</div>
                </div>
                <div className="text-gray-400">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </div>
              </div>
            )
          })}
        </div>
      </div>
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <p className="text-xs text-gray-600">
          <span className="font-medium">Tip:</span> Drag components to the canvas to build your workflow
        </p>
      </div>
    </div>
  )
}

export default ComponentSidebar