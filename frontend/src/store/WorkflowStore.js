import { create } from 'zustand'

const useWorkflowStore = create((set, get) => ({
  workflows: [],
  currentWorkflow: null,
  
  nodes: [],
  edges: [],
  
  isSaving: false,
  
  setWorkflows: (workflows) => set({ workflows }),
  
  setCurrentWorkflow: (workflow) => set({ 
    currentWorkflow: workflow,
    nodes: Array.isArray(workflow?.nodes) ? workflow.nodes : [],
    edges: Array.isArray(workflow?.edges) ? workflow.edges : []
  }),
  
  setNodes: (nodesOrUpdater) => set((state) => ({
    nodes: typeof nodesOrUpdater === 'function' 
      ? nodesOrUpdater(state.nodes) 
      : (Array.isArray(nodesOrUpdater) ? nodesOrUpdater : [])
  })),
  
  setEdges: (edgesOrUpdater) => set((state) => ({
    edges: typeof edgesOrUpdater === 'function' 
      ? edgesOrUpdater(state.edges) 
      : (Array.isArray(edgesOrUpdater) ? edgesOrUpdater : [])
  })),
  
  addNode: (node) => set((state) => ({
    nodes: [...state.nodes, node]
  })),
  
  updateNode: (nodeId, data) => set((state) => ({
    nodes: state.nodes.map(node => 
      node.id === nodeId ? { ...node, data: { ...node.data, ...data } } : node
    )
  })),
  
  deleteNode: (nodeId) => set((state) => ({
    nodes: state.nodes.filter(node => node.id !== nodeId),
    edges: state.edges.filter(edge => edge.source !== nodeId && edge.target !== nodeId)
  })),
  
  addEdge: (edge) => set((state) => ({
    edges: [...state.edges, edge]
  })),
  
  deleteEdge: (edgeId) => set((state) => ({
    edges: state.edges.filter(edge => edge.id !== edgeId)
  })),
  
  clearWorkflow: () => set({
    currentWorkflow: null,
    nodes: [],
    edges: []
  }),
  
  setSaving: (isSaving) => set({ isSaving })
}))

export default useWorkflowStore