import React from 'react'
import { useAuthStore } from '../stores/authStore'
import { Navigate } from 'react-router-dom'

export const DashboardPage: React.FC = () => {
  const user = useAuthStore((state) => state.user)
  const clearAuth = useAuthStore((state) => state.clearAuth)

  if (!user) {
    return <Navigate to="/login" />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold">LegalFlow AI</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">{user.full_name}</span>
              <button
                onClick={() => clearAuth()}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Выход
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4">
              Добро пожаловать в LegalFlow AI!
            </h2>
            <p className="text-gray-600">
              Платформа для автоматизации юридического бизнеса
            </p>
            
            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
              <a
                href="/chat"
                className="border rounded-lg p-4 hover:shadow-lg transition cursor-pointer"
              >
                <h3 className="font-semibold mb-2">🤖 AI Консультант</h3>
                <p className="text-sm text-gray-600">
                  Умный чат-бот для консультаций клиентов
                </p>
                <span className="text-xs text-blue-600 mt-2 inline-block">
                  Открыть чат →
                </span>
              </a>
              
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">📄 Анализ документов</h3>
                <p className="text-sm text-gray-600">
                  Автоматический анализ договоров и документов
                </p>
              </div>
              
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold mb-2">🔗 CRM интеграция</h3>
                <p className="text-sm text-gray-600">
                  Синхронизация с AmoCRM и Bitrix24
                </p>
              </div>
            </div>
            
            <div className="mt-8">
              <h3 className="font-semibold mb-4">Этап 1: Инфраструктура ✅</h3>
              <ul className="list-disc list-inside space-y-2 text-sm text-gray-600">
                <li>FastAPI backend с JWT авторизацией</li>
                <li>React frontend с TypeScript</li>
                <li>MySQL + Redis</li>
                <li>Docker Compose</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

