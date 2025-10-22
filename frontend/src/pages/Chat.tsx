import React, { useState, useRef, useEffect } from 'react'
import { useAuthStore } from '../stores/authStore'
import { Navigate } from 'react-router-dom'
import { useStreamingChat } from '../hooks/useChat'
import { ChatMessage } from '../services/llm'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export const ChatPage: React.FC = () => {
  const user = useAuthStore((state) => state.user)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [selectedModel, setSelectedModel] = useState('gpt-3.5-turbo')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const { streamingContent, isStreaming, streamChat } = useStreamingChat()

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, streamingContent])

  if (!user) {
    return <Navigate to="/login" />
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim() || isStreaming) return

    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')

    // Stream response
    await streamChat({
      messages: [...messages, userMessage],
      model: selectedModel,
      temperature: 0.7,
      max_tokens: 2000,
    })

    // Add assistant response to messages
    if (streamingContent) {
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: streamingContent,
      }
      setMessages((prev) => [...prev, assistantMessage])
    }
  }

  // When streaming completes, add to messages
  useEffect(() => {
    if (!isStreaming && streamingContent) {
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: streamingContent,
      }
      setMessages((prev) => {
        // Check if already added
        const lastMsg = prev[prev.length - 1]
        if (lastMsg?.role === 'assistant' && lastMsg.content === streamingContent) {
          return prev
        }
        return [...prev, assistantMessage]
      })
    }
  }, [isStreaming, streamingContent])

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">🤖 AI Консультант</h1>
          <div className="flex items-center space-x-4">
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="text-sm border rounded px-2 py-1"
            >
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4-turbo-preview">GPT-4 Turbo</option>
            </select>
            <a href="/dashboard" className="text-sm text-gray-600 hover:text-gray-900">
              ← Назад
            </a>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-12">
              <p className="text-lg">Задайте вопрос юридическому ассистенту</p>
              <p className="text-sm mt-2">Например: "Как расторгнуть договор аренды?"</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl rounded-lg px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border shadow-sm'
                }`}
              >
                {msg.role === 'assistant' ? (
                  <div className="prose prose-sm max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                )}
              </div>
            </div>
          ))}

          {/* Streaming message */}
          {isStreaming && streamingContent && (
            <div className="flex justify-start">
              <div className="max-w-3xl rounded-lg px-4 py-3 bg-white border shadow-sm">
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {streamingContent}
                  </ReactMarkdown>
                </div>
                <div className="mt-2 flex items-center text-xs text-gray-500">
                  <div className="animate-pulse">●</div>
                  <span className="ml-2">Печатает...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-white border-t">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Введите ваш вопрос..."
              disabled={isStreaming}
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isStreaming || !input.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isStreaming ? '...' : 'Отправить'}
            </button>
          </form>
          <p className="text-xs text-gray-500 mt-2">
            Используйте AI для получения общей юридической информации.
            Для сложных случаев обратитесь к юристу.
          </p>
        </div>
      </div>
    </div>
  )
}

