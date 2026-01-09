import React, { useState, useEffect } from 'react'
import { Plus } from 'lucide-react'
import Header from '../components/layout/Header'
import StackCard from '../components/dashboard/StackCard'
import EmptyState from '../components/dashboard/EmptyState'
import CreateStackModal from '../components/dashboard/CreateStackModal'
import Button from '../components/ui/Button'
import { workflowAPI } from '../services/api'
import useWorkflowStore from '../store/WorkflowStore'

const Dashboard = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [loading, setLoading] = useState(true)
  const { workflows, setWorkflows } = useWorkflowStore()

  useEffect(() => {
    loadWorkflows()
  }, [])

  const loadWorkflows = async () => {
    try {
      setLoading(true)
      const data = await workflowAPI.list()
      setWorkflows(data)
    } catch (error) {
      console.error('Failed to load workflows:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateStack = async (formData) => {
    try {
      const newWorkflow = {
        name: formData.name,
        description: formData.description,
        nodes: [],
        edges: []
      }
      await workflowAPI.create(newWorkflow)
      await loadWorkflows()
      setIsModalOpen(false)
    } catch (error) {
      console.error('Failed to create workflow:', error)
      alert('Failed to create stack. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Stacks</h1>
          {workflows.length > 0 && (
            <Button icon={Plus} onClick={() => setIsModalOpen(true)}>
              New Stack
            </Button>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : workflows.length === 0 ? (
          <EmptyState onCreateNew={() => setIsModalOpen(true)} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {workflows.map((workflow) => (
              <StackCard key={workflow.id} stack={workflow} onDelete={loadWorkflows} />
            ))}
          </div>
        )}
      </main>

      <CreateStackModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateStack}
      />
    </div>
  )
}

export default Dashboard