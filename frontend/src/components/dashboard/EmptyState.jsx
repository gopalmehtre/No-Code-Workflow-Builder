import React from 'react'
import { Plus } from 'lucide-react'
import Button from '../ui/Button'

const EmptyState = ({ onCreateNew }) => {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="text-center bg-white rounded-lg shadow-sm p-8 max-w-md">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Create New Stack
        </h2>
        <p className="text-gray-600 mb-6">
          Start building your generative AI apps with our essential tools and frameworks
        </p>
        <Button icon={Plus} onClick={onCreateNew}>
          New Stack
        </Button>
      </div>
    </div>
  )
}

export default EmptyState