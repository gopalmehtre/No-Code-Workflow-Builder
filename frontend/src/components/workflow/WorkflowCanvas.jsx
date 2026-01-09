import React, { useCallback, useMemo } from 'react'
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  MarkerType
} from 'reactflow'
import 'reactflow/dist/style.css'
import useWorkflowStore from '../../store/WorkflowStore'
import UserQueryNode from '../nodes/UserQueryNode'
import KnowledgeBaseNode from '../nodes/KnowledgeBaseNode'
import LLMNode from '../nodes/LLMNode'
import OutputNode from '../nodes/OutputNode'

const WorkflowCanvas = () => {
  const { nodes, edges, setNodes, setEdges, updateNode } = useWorkflowStore()

  const nodeTypes = useMemo(() => ({
    user_query: UserQueryNode,
    knowledge_base: KnowledgeBaseNode,
    llm_engine: LLMNode,
    output: OutputNode
  }), [])

  const nodesWithCallbacks = useMemo(() => {
    return nodes.map(node => ({
      ...node,
      data: {
        ...node.data,
        onChange: (newData) => updateNode(node.id, newData)
      }
    }))
  }, [nodes, updateNode])

  const onNodesChange = useCallback((changes) => {
    setNodes((nds) => {
      const updatedNodes = changes.reduce((acc, change) => {
        if (change.type === 'remove') {
          return acc.filter(node => node.id !== change.id)
        }
        if (change.type === 'position' && change.position) {
          return acc.map(node =>
            node.id === change.id
              ? { ...node, position: change.position, dragging: change.dragging }
              : node
          )
        }
        if (change.type === 'dimensions' && change.dimensions) {
          return acc.map(node =>
            node.id === change.id ? { ...node, ...change.dimensions } : node
          )
        }
        return acc
      }, nds)
      return updatedNodes
    })
  }, [setNodes])

  const onEdgesChange = useCallback((changes) => {
    setEdges((eds) => {
      const updatedEdges = changes.reduce((acc, change) => {
        if (change.type === 'remove') {
          return acc.filter(edge => edge.id !== change.id)
        }
        if (change.type === 'select') {
          return acc.map(edge =>
            edge.id === change.id ? { ...edge, selected: change.selected } : edge
          )
        }
        return acc
      }, eds)
      return updatedEdges
    })
  }, [setEdges])

  const onConnect = useCallback((params) => {
    const newEdge = {
      ...params,
      type: 'smoothstep',
      animated: true,
      markerEnd: {
        type: MarkerType.ArrowClosed,
      },
      style: { strokeWidth: 2 }
    }
    setEdges((eds) => addEdge(newEdge, eds))
  }, [setEdges])

  const onDragOver = useCallback((event) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  const onDrop = useCallback((event) => {
    event.preventDefault()

    const type = event.dataTransfer.getData('application/reactflow')
    if (!type) return

    const position = {
      x: event.clientX - 250,
      y: event.clientY - 100
    }

    const nodeId = `${type}-${Date.now()}`

    const newNode = {
      id: nodeId,
      type,
      position,
      data: {
        label: type,
        onChange: (newData) => updateNode(nodeId, newData)
      },
      selectable: true,
      deletable: true
    }

    setNodes((nds) => [...nds, newNode])
  }, [updateNode, setNodes])

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodesWithCallbacks}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onDrop={onDrop}
        onDragOver={onDragOver}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
        deleteKeyCode="Delete"
        multiSelectionKeyCode="Control"
        selectNodesOnDrag={false}
      >
        <Background color="#e5e7eb" gap={16} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            switch (node.type) {
              case 'user_query': return '#f59e0b'
              case 'knowledge_base': return '#3b82f6'
              case 'llm_engine': return '#8b5cf6'
              case 'output': return '#10b981'
              default: return '#6b7280'
            }
          }}
        />
      </ReactFlow>
    </div>
  )
}

export default WorkflowCanvas