import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { BookOpen, Settings, Upload, X } from 'lucide-react'
import { documentsAPI } from '../../services/api'

const KnowledgeBaseNode = ({ data, isConnectable }) => {
  const [showConfig, setShowConfig] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(data.uploadedFile || (data.collection_name ? { collectionName: data.collection_name } : null))
  
  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    
    setUploading(true)
    try {
      const result = await documentsAPI.upload(file)
      setUploadedFile({
        name: file.name,
        collectionName: result.document.collection_name
      })
      data.onChange?.({ 
        collection_name: result.document.collection_name,
        uploadedFile: { name: file.name }
      })
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Failed to upload file')
    } finally {
      setUploading(false)
    }
  }
  
  const handleRemoveFile = () => {
    setUploadedFile(null)
    data.onChange?.({ collection_name: null, uploadedFile: null })
  }
  
  return (
    <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200 min-w-[280px]">
      {/* Header */}
      <div className="flex items-center justify-between p-3 border-b bg-gray-50">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-gray-600" />
          <span className="font-medium text-sm">Knowledge Base</span>
        </div>
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="p-1 hover:bg-gray-200 rounded transition-colors"
        >
          <Settings className="w-4 h-4" />
        </button>
      </div>
      
      {/* Content */}
      <div className="p-3">
        <p className="text-xs text-gray-600 mb-2">Let LLM search info in your file</p>
        
        {showConfig && (
          <div className="mt-2 space-y-3">
            {/* File Upload */}
            <div>
              <label className="block text-xs text-gray-700 mb-1">
                File for Knowledge Base
              </label>
              
              {uploadedFile ? (
                <div className="flex items-center justify-between p-2 bg-green-50 border border-green-200 rounded">
                  <span className="text-xs text-green-700">{uploadedFile.name}</span>
                  <button
                    onClick={handleRemoveFile}
                    className="p-1 hover:bg-green-100 rounded"
                  >
                    <X className="w-3 h-3 text-green-700" />
                  </button>
                </div>
              ) : (
                <label className="flex flex-col items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded cursor-pointer hover:border-primary-500 transition-colors">
                  <Upload className="w-6 h-6 text-gray-400 mb-1" />
                  <span className="text-xs text-primary-600">Upload File</span>
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileUpload}
                    disabled={uploading}
                    className="hidden"
                  />
                </label>
              )}
              
              {uploading && (
                <p className="text-xs text-gray-500 mt-1">Uploading...</p>
              )}
            </div>
            
            {/* Embedding Model */}
            <div>
              <label className="block text-xs text-gray-700 mb-1">
                Embedding Model
              </label>
              <select className="w-full px-2 py-1 text-sm border rounded focus:outline-none focus:ring-1 focus:ring-primary-500">
                <option>text-embedding-004</option>
              </select>
            </div>
          </div>
        )}
      </div>
      
      {/* Handles */}
      <Handle
        type="target"
        position={Position.Left}
        id="query"
        style={{ background: '#f59e0b' }}
        isConnectable={isConnectable}
      />
      <Handle
        type="source"
        position={Position.Right}
        id="context"
        style={{ background: '#ef4444' }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default KnowledgeBaseNode