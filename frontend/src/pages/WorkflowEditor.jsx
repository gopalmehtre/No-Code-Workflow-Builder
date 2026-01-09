import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Play, MessageSquare } from 'lucide-react'
import Header from '../components/layout/Header'
import ComponentSidebar from '../components/workflow/ComponentSidebar'
import WorkflowCanvas from '../components/workflow/WorkflowCanvas'
import ChatModal from '../components/chat/ChatModal'
import useWorkflowStore from '../store/WorkflowStore'
import { workflowAPI } from '../services/api'

const WorkflowEditor = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [isExecuting, setIsExecuting] = useState(false)
  const { currentWorkflow, setCurrentWorkflow, nodes, edges, setSaving } = useWorkflowStore()

  useEffect(() => {
    if (id && id !== 'new') {
      loadWorkflow(id)
    } else {
      setCurrentWorkflow(null)
    }
  }, [id])

  const loadWorkflow = async (workflowId) => {
    try {
      const workflow = await workflowAPI.get(workflowId)
      setCurrentWorkflow(workflow)
    } catch (error) {
      console.error('Failed to load workflow:', error)
      alert('Failed to load workflow')
      navigate('/')
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      const workflowData = {
        name: currentWorkflow?.name || 'Untitled Workflow',
        description: currentWorkflow?.description || '',
        nodes: nodes,
        edges: edges
      }

      if (id && id !== 'new') {
        await workflowAPI.update(id, workflowData)
      } else {
        const created = await workflowAPI.create(workflowData)
        navigate(`/workflow/${created.id}`, { replace: true })
      }
      
      alert('Workflow saved successfully!')
    } catch (error) {
      console.error('Failed to save workflow:', error)
      alert('Failed to save workflow. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const handleExecute = async () => {
    if (!id || id === 'new') {
      alert('Please save the workflow first')
      return
    }

    const query = prompt('Enter your question:')
    if (!query || !query.trim()) {
      return
    }

    try {
      setIsExecuting(true)
      
      console.log('Executing workflow with:', {
        nodes: nodes,
        edges: edges,
        query: query.trim(),
        workflow_id: parseInt(id)
      })
      
      const result = await workflowAPI.execute({
        nodes: nodes,
        edges: edges,
        query: query.trim(),
        workflow_id: parseInt(id)
      })
      
      console.log('Execution result:', result)
      
      if (result.success) {
        alert(`Success!\n\nQuery: ${result.query}\n\nResponse: ${result.response}`)
      } else {
        alert(`Error!\n\n${result.error || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Execution failed:', error)
      console.error('Error details:', error.response?.data)
      alert(`Workflow execution failed.\n\nError: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsExecuting(false)
    }
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header showSave onSave={handleSave} />
      
      <div className="flex-1 flex overflow-hidden">
        <ComponentSidebar workflowName={currentWorkflow?.name || 'Untitled'} />
        
        <div className="flex-1 relative">
          <WorkflowCanvas />
          <div className="absolute bottom-6 right-6 flex flex-col gap-3">
            <button
              onClick={handleExecute}
              disabled={isExecuting}
              className="w-14 h-14 bg-primary-500 hover:bg-primary-600 text-white rounded-full shadow-lg flex items-center justify-center transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              title="Run Workflow"
            >
              <Play className="w-6 h-6" fill="currentColor" />
            </button>
            
            <button
              onClick={() => setIsChatOpen(true)}
              className="w-14 h-14 bg-blue-500 hover:bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center transition-all"
              title="Chat with Stack"
            >
              <MessageSquare className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      <ChatModal
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        workflowId={id}
      />
    </div>
  )
}

export default WorkflowEditor