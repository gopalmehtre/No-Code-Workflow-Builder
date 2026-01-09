import { create } from 'zustand'

const useChatStore = create((set) => ({
  messages: [],
  isOpen: false,
  isLoading: false,
  
  setMessages: (messages) => set({ messages }),
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),
  
  clearMessages: () => set({ messages: [] }),
  
  openChat: () => set({ isOpen: true }),
  closeChat: () => set({ isOpen: false }),
  
  setLoading: (isLoading) => set({ isLoading })
}))

export default useChatStore