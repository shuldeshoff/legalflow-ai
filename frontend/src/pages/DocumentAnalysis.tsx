import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { documentApi, type DocumentAnalysis } from '../services/documents';

export default function DocumentAnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [document, setDocument] = useState<DocumentAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (id) {
      loadDocument(parseInt(id));
    }
  }, [id]);

  const loadDocument = async (docId: number) => {
    try {
      setLoading(true);
      const data = await documentApi.get(docId);
      setDocument(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки документа');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    const colors = {
      low: 'text-yellow-700 bg-yellow-50 border-yellow-200',
      medium: 'text-orange-700 bg-orange-50 border-orange-200',
      high: 'text-red-700 bg-red-50 border-red-200',
    };
    return colors[severity as keyof typeof colors] || colors.low;
  };

  const getSeverityIcon = (severity: string) => {
    const icons = {
      low: '⚠️',
      medium: '⚡',
      high: '🚨',
    };
    return icons[severity as keyof typeof icons] || '⚠️';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Загрузка...</div>
      </div>
    );
  }

  if (error || !document) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Документ не найден'}</p>
          <button
            onClick={() => navigate('/documents')}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Вернуться к документам
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/documents')}
            className="text-blue-600 hover:text-blue-700 mb-4 inline-flex items-center"
          >
            ← Назад к документам
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{document.title}</h1>
          <div className="flex items-center gap-2 text-gray-600">
            <span className={`px-3 py-1 rounded text-sm font-medium ${
              document.analysis_status === 'completed' ? 'bg-green-100 text-green-800' :
              document.analysis_status === 'processing' ? 'bg-blue-100 text-blue-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {document.analysis_status === 'completed' ? '✓ Анализ завершен' :
               document.analysis_status === 'processing' ? '⟳ Обработка' :
               'Ожидает анализа'}
            </span>
            {document.analyzed_at && (
              <span className="text-sm">
                {new Date(document.analyzed_at).toLocaleString('ru-RU')}
              </span>
            )}
          </div>
        </div>

        {document.analysis_status !== 'completed' ? (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <p className="text-gray-600 mb-4">
              {document.analysis_status === 'processing' 
                ? 'Документ обрабатывается. Пожалуйста, подождите...'
                : 'Документ еще не проанализирован.'}
            </p>
            <button
              onClick={() => navigate('/documents')}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Вернуться к документам
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Summary */}
            {document.analysis_summary && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  📝 Краткое содержание
                </h2>
                <p className="text-gray-700 leading-relaxed">{document.analysis_summary}</p>
              </div>
            )}

            {/* Key Points */}
            {document.key_points && document.key_points.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  🔑 Ключевые пункты
                </h2>
                <ul className="space-y-3">
                  {document.key_points.map((point, index) => (
                    <li key={index} className="flex gap-3">
                      <span className="text-blue-600 font-semibold">{index + 1}.</span>
                      <span className="text-gray-700">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Risks */}
            {document.risks && document.risks.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  ⚠️ Выявленные риски
                </h2>
                <div className="space-y-4">
                  {document.risks.map((risk, index) => (
                    <div
                      key={index}
                      className={`border rounded-lg p-4 ${getSeverityColor(risk.severity)}`}
                    >
                      <div className="flex items-start gap-3 mb-2">
                        <span className="text-2xl">{getSeverityIcon(risk.severity)}</span>
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg mb-1">{risk.type}</h3>
                          <p className="text-sm mb-3">{risk.description}</p>
                          <div className="bg-white bg-opacity-50 rounded p-3">
                            <p className="text-sm font-medium mb-1">💡 Рекомендация:</p>
                            <p className="text-sm">{risk.recommendation}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {document.recommendations && (
              <div className="bg-blue-50 rounded-lg shadow-sm p-6 border border-blue-200">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-blue-900">
                  💡 Общие рекомендации
                </h2>
                <p className="text-blue-900 leading-relaxed">{document.recommendations}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

