import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

export default function Dashboard() {
  const { user, logout } = useAuthStore();

  const features = [
    {
      title: '🤖 AI Консультант',
      description: 'Получите ответы на юридические вопросы с помощью AI',
      link: '/chat',
      color: 'bg-blue-500 hover:bg-blue-600',
    },
    {
      title: '📄 Анализ документов',
      description: 'Загрузите документ для AI-анализа рисков и ключевых пунктов',
      link: '/documents',
      color: 'bg-green-500 hover:bg-green-600',
    },
    {
      title: '📚 База знаний',
      description: 'Поиск информации в юридической базе знаний с RAG',
      link: '/knowledge',
      color: 'bg-purple-500 hover:bg-purple-600',
    },
  ];

  const stats = [
    { label: 'Обработано документов', value: '—', icon: '📊' },
    { label: 'Консультаций', value: '—', icon: '💬' },
    { label: 'База знаний', value: '—', icon: '📖' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">⚖️ LegalFlow AI</h1>
            <p className="text-sm text-gray-600">Платформа для автоматизации юридических процессов</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">{user?.email}</p>
              <p className="text-xs text-gray-500">Пользователь</p>
            </div>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white text-sm rounded hover:bg-red-700"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Добро пожаловать, {user?.email?.split('@')[0]}! 👋
          </h2>
          <p className="text-gray-600">
            Выберите функцию для работы с AI-платформой
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-3xl">{stat.icon}</span>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {features.map((feature, index) => (
            <Link
              key={index}
              to={feature.link}
              className={`${feature.color} text-white rounded-lg shadow-lg p-6 transform transition hover:scale-105`}
            >
              <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
              <p className="text-white text-opacity-90">{feature.description}</p>
              <div className="mt-4 flex items-center text-white text-opacity-90">
                <span className="mr-2">Открыть</span>
                <span>→</span>
              </div>
            </Link>
          ))}
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-xl font-semibold mb-3">🚀 Возможности платформы</h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>AI-консультации по юридическим вопросам</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Автоматический анализ документов с выявлением рисков</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>RAG-система для точных ответов из базы знаний</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Поддержка PDF, DOCX и TXT документов</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Streaming ответов в реальном времени</span>
              </li>
            </ul>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3 text-blue-900">💡 Как начать работу</h3>
            <ol className="space-y-3 text-blue-900">
              <li className="flex gap-3">
                <span className="font-bold">1.</span>
                <span>Задайте вопрос AI-консультанту или загрузите документ</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold">2.</span>
                <span>Получите AI-анализ с рисками и рекомендациями</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold">3.</span>
                <span>Используйте базу знаний для поиска информации</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold">4.</span>
                <span>Все результаты сохраняются в вашем аккаунте</span>
              </li>
            </ol>
          </div>
        </div>

        {/* Tech Stack Info */}
        <div className="mt-8 bg-gray-800 text-white rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-3">🔧 Технологии</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="font-semibold mb-1">Backend</p>
              <p className="text-gray-300">Python FastAPI</p>
            </div>
            <div>
              <p className="font-semibold mb-1">Frontend</p>
              <p className="text-gray-300">React + TypeScript</p>
            </div>
            <div>
              <p className="font-semibold mb-1">AI/LLM</p>
              <p className="text-gray-300">OpenAI GPT-4, Yandex GPT</p>
            </div>
            <div>
              <p className="font-semibold mb-1">Vector DB</p>
              <p className="text-gray-300">ChromaDB</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
