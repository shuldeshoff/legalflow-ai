import { useState, useRef } from 'react'
import { useMutation } from '@tanstack/react-query'
import { llmApi, ChatRequest } from '../services/llm'

export const useStreamingChat = () => {
  const [streamingContent, setStreamingContent] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)

  const streamChat = async (request: ChatRequest) => {
    setIsStreaming(true)
    setStreamingContent('')
    
    abortControllerRef.current = new AbortController()
    
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('/api/v1/llm/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(request),
        signal: abortControllerRef.current.signal,
      })

      if (!response.ok) {
        throw new Error('Stream failed')
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('No reader available')
      }

      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              
              if (data.content) {
                setStreamingContent((prev) => prev + data.content)
              }
              
              if (data.done) {
                setIsStreaming(false)
                return
              }
            } catch (e) {
              console.error('Parse error:', e)
            }
          }
        }
      }
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        console.error('Stream error:', error)
      }
    } finally {
      setIsStreaming(false)
    }
  }

  const stopStreaming = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      setIsStreaming(false)
    }
  }

  return {
    streamingContent,
    isStreaming,
    streamChat,
    stopStreaming,
  }
}

export const useChat = () => {
  const chatMutation = useMutation({
    mutationFn: llmApi.chat,
  })

  return {
    chat: chatMutation.mutate,
    isLoading: chatMutation.isPending,
    error: chatMutation.error,
    data: chatMutation.data,
  }
}

