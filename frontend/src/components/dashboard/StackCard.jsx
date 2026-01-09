import React from 'react'
import { ExternalLink, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { workflowAPI } from '../../services/api'

const StackCard = ({ stack, onDelete }) => {
  const navigate = useNavigate()

  const handleDelete = async(e) => {
    e.stopPropagation()

    if(window.confirm(`Are you sure you want to delete "${stack.name}"? `))
      try {
        await workflowAPI.delete(stack.id)
        if(onDelete){
          onDelete(stack.id)
        }
    } catch(err){
      console.error('Failed to delete workflow :', err)
      alert('Failed to delete workflow. Please try again.')
    }
  }
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className='flex items-start justify-between mb-2'>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {stack.name}
      </h3>
      <button onClick={handleDelete}
      className="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-50 transition-colors"
          title="Delete workflow">
        <Trash2 className="w-4 h-4"/>
      </button>
      </div>

      <p className="text-gray-600 text-sm mb-4">
        {stack.description || 'No description'}
      </p>
      
      <button
        onClick={() => navigate(`/workflow/${stack.id}`)}
        className="inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium text-sm"
      >
        Edit Stack
        <ExternalLink className="w-4 h-4" />
      </button>
    </div>
  )
}

export default StackCard