import { useState, useEffect } from 'react';
import { knowledgeApi, type KnowledgeBase, type RAGResponse } from '../services/knowledge';

export default function KnowledgePage() {
  const [knowledge, setKnowledge] = useState<KnowledgeBase[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [ragResponse, setRagResponse] = useState<RAGResponse | null>(null);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadKnowledge();
  }, []);

  const loadKnowledge = async () => {
    try {
      setLoading(true);
      const data = await knowledgeApi.list();
      setKnowledge(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки базы знаний');
    } finally {
      setLoading(false);
    }
  };

  const handleRAGQuery = async () => {
    if (!query.trim()) return;

    try {
      setSearching(true);
      setError('');
      const response = await knowledgeApi.ragQuery(query);
      setRagResponse(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка выполнения запроса');
    } finally {
      setSearching(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleRAGQuery();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📚 База знаний</h1>
          <p className="text-gray-600">Поиск и консультации на основе юридической базы знаний с RAG</p>
        </div>

        {/* RAG Query Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">🤖 Задайте вопрос</h2>
          <p className="text-sm text-gray-600 mb-4">
            Система найдет релевантную информацию в базе знаний и сгенерирует точный ответ с указанием источников
          </p>

          <div className="space-y-4">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Например: Каковы основные условия трудового договора?"
              className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button
              onClick={handleRAGQuery}
              disabled={!query.trim() || searching}
              className="w-full md:w-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {searching ? 'Поиск и генерация ответа...' : 'Получить ответ'}
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded text-red-700">
              {error}
            </div>
          )}

          {/* RAG Response */}
          {ragResponse && (
            <div className="mt-6 space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-3 text-blue-900">💬 Ответ:</h3>
                <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {ragResponse.answer}
                </p>
              </div>

              {ragResponse.sources && ragResponse.sources.length > 0 && (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold mb-3 text-gray-900">📖 Источники:</h3>
                  <div className="space-y-2">
                    {ragResponse.sources.map((source, index) => (
                      <div key={index} className="flex items-start gap-3">
                        <span className="text-blue-600 font-semibold">[{index + 1}]</span>
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">{source.title}</p>
                          {source.category && (
                            <span className="text-sm text-gray-600">
                              Категория: {source.category}
                            </span>
                          )}
                          <span className="text-sm text-gray-500 ml-3">
                            Релевантность: {(source.score * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="text-sm text-gray-500">
                Модель: {ragResponse.model} | 
                Токены: {ragResponse.usage?.total_tokens || 0}
              </div>
            </div>
          )}
        </div>

        {/* Knowledge Base List */}
        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold">Документы в базе знаний</h2>
          </div>

          {loading ? (
            <div className="p-8 text-center text-gray-500">Загрузка...</div>
          ) : knowledge.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              База знаний пуста. Добавьте документы через админ-панель.
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {knowledge.map((item) => (
                <div key={item.id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">{item.title}</h3>
                      
                      <p className="text-gray-700 mb-3 line-clamp-3">{item.content}</p>
                      
                      <div className="flex flex-wrap gap-3 text-sm text-gray-600">
                        {item.category && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                            {item.category}
                          </span>
                        )}
                        {item.source && (
                          <span className="flex items-center gap-1">
                            🔗 {item.source}
                          </span>
                        )}
                        <span>📅 {new Date(item.created_at).toLocaleDateString('ru-RU')}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Info Section */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-2 text-blue-900">ℹ️ О базе знаний</h3>
          <p className="text-blue-800 mb-2">
            База знаний использует RAG (Retrieval Augmented Generation) для точных ответов на юридические вопросы.
          </p>
          <ul className="list-disc list-inside text-blue-800 space-y-1">
            <li>Семантический поиск по содержанию документов</li>
            <li>AI генерирует ответы на основе найденного контекста</li>
            <li>Указание источников для проверки информации</li>
            <li>Работает с документами любого размера</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

