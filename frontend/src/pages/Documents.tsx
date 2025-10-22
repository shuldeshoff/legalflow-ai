import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { documentApi, type Document, type DocumentAnalysis } from '../services/documents';

export default function DocumentsPage() {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState<number | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(true);

  // Load documents on mount
  useState(() => {
    loadDocuments();
  });

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const data = await documentApi.list();
      setDocuments(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки документов');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      if (!validTypes.includes(file.type)) {
        setError('Поддерживаются только PDF, DOCX и TXT файлы');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setUploading(true);
      setError('');
      const doc = await documentApi.upload(selectedFile);
      setDocuments([doc, ...documents]);
      setSelectedFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка загрузки файла');
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async (docId: number) => {
    try {
      setAnalyzing(docId);
      setError('');
      await documentApi.analyze(docId);
      await loadDocuments(); // Refresh list
      // Navigate to analysis page
      navigate(`/documents/${docId}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка анализа документа');
    } finally {
      setAnalyzing(null);
    }
  };

  const handleDelete = async (docId: number) => {
    if (!confirm('Удалить документ?')) return;

    try {
      await documentApi.delete(docId);
      setDocuments(documents.filter(d => d.id !== docId));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка удаления документа');
    }
  };

  const getStatusBadge = (status?: string) => {
    const styles = {
      pending: 'bg-gray-100 text-gray-800',
      processing: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    };

    const labels = {
      pending: 'Ожидает',
      processing: 'Обработка',
      completed: 'Готов',
      failed: 'Ошибка',
    };

    const style = styles[status as keyof typeof styles] || styles.pending;
    const label = labels[status as keyof typeof labels] || status;

    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${style}`}>
        {label}
      </span>
    );
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '-';
    const kb = bytes / 1024;
    if (kb < 1024) return `${kb.toFixed(1)} KB`;
    return `${(kb / 1024).toFixed(1)} MB`;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">📄 Документы</h1>
          <p className="text-gray-600">Загрузка и AI-анализ юридических документов</p>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Загрузить документ</h2>
          
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <label htmlFor="file-input" className="block text-sm font-medium text-gray-700 mb-2">
                Выберите файл (PDF, DOCX, TXT)
              </label>
              <input
                id="file-input"
                type="file"
                onChange={handleFileSelect}
                accept=".pdf,.docx,.txt"
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
              {selectedFile && (
                <p className="mt-2 text-sm text-gray-600">
                  Выбран: {selectedFile.name} ({formatFileSize(selectedFile.size)})
                </p>
              )}
            </div>
            
            <div className="flex items-end">
              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {uploading ? 'Загрузка...' : 'Загрузить'}
              </button>
            </div>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded text-red-700">
              {error}
            </div>
          )}
        </div>

        {/* Documents List */}
        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold">Ваши документы</h2>
          </div>

          {loading ? (
            <div className="p-8 text-center text-gray-500">Загрузка...</div>
          ) : documents.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              Нет документов. Загрузите первый документ выше.
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {documents.map((doc) => (
                <div key={doc.id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-medium text-gray-900">{doc.title}</h3>
                        {getStatusBadge(doc.analysis_status)}
                      </div>
                      
                      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                        <span>📎 {doc.file_type?.toUpperCase()}</span>
                        <span>💾 {formatFileSize(doc.file_size)}</span>
                        <span>📅 {new Date(doc.uploaded_at).toLocaleDateString('ru-RU')}</span>
                      </div>
                    </div>

                    <div className="flex gap-2 ml-4">
                      {doc.analysis_status === 'completed' ? (
                        <button
                          onClick={() => navigate(`/documents/${doc.id}`)}
                          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                        >
                          Просмотр
                        </button>
                      ) : doc.analysis_status === 'pending' ? (
                        <button
                          onClick={() => handleAnalyze(doc.id)}
                          disabled={analyzing === doc.id}
                          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300"
                        >
                          {analyzing === doc.id ? 'Анализ...' : 'Анализировать'}
                        </button>
                      ) : doc.analysis_status === 'processing' ? (
                        <button
                          disabled
                          className="px-4 py-2 bg-gray-300 text-gray-600 rounded cursor-not-allowed"
                        >
                          Обработка...
                        </button>
                      ) : null}
                      
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                      >
                        Удалить
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

