import api from '../lib/api'

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  messages: ChatMessage[]
  model?: string
  temperature?: number
  max_tokens?: number
  stream?: boolean
}

export interface ChatResponse {
  content: string
  model: string
  provider: string
  usage: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
  finish_reason: string
}

export const llmApi = {
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/llm/chat', request)
    return response.data
  },
  
  streamChat: (request: ChatRequest): EventSource => {
    const token = localStorage.getItem('access_token')
    const url = new URL('/api/v1/llm/chat/stream', window.location.origin)
    
    // For EventSource, we need to pass data via URL params or use a different approach
    // We'll use fetch with ReadableStream instead
    return new EventSource(url.toString(), {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
  },
  
  getModels: async () => {
    const response = await api.get('/llm/models')
    return response.data
  },
}

