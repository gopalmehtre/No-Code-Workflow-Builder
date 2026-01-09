import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

export const documentsAPI = {
    upload: async (file) => {
        const formData = new FormData()
        formData.append('file', file)
        const response = await api.post('/documents/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        return response.data
    },

    list: async () => {
        const response = await api.get('/documents/')
        return response.data
    },

    get: async (id) => {
        const response = await api.get(`/documents/${id}`)
        return response.data
    },
}

export const workflowAPI = {
    list: async () => {
        const response = await api.get('/workflow/')
        return response.data
    },

    get: async (id) => {
        const response = await api.get(`/workflow/${id}`)
        return response.data
    },

    create: async (data) => {
        const response = await api.post('/workflow/save', data)
        return response.data
    },

    update: async (id, data) => {
        const response = await api.put(`/workflow/${id}`, data)
        return response.data
    },

    delete: async (id) => {
        const response = await api.delete(`/workflow/${id}`)
        return response.data
    },

    validate: async (data) => {
        const response = await api.post('/workflow/validate', data)
        return response.data
    },

    execute: async (data) => {
        const response = await api.post('/workflow/execute', data)
        return response.data
    }
}

export const chatAPI = {
    send: async (workflowId, query) => {
        const response = await api.post('/chat', { workflow_id: workflowId, query })
        return response.data
    }
}

export default api