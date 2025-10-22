import api from '../lib/api';

export interface Document {
  id: number;
  title: string;
  file_path: string;
  file_type?: string;
  file_size?: number;
  uploaded_at: string;
  client_id?: number;
  uploaded_by?: number;
  analysis_status?: string;
}

export interface DocumentAnalysis {
  id: number;
  title: string;
  analysis_status: string;
  analysis_summary?: string;
  key_points?: string[];
  risks?: Array<{
    type: string;
    description: string;
    severity: 'low' | 'medium' | 'high';
    recommendation: string;
  }>;
  recommendations?: string;
  analyzed_at?: string;
}

export const documentApi = {
  async upload(file: File, clientId?: number): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);
    if (clientId) {
      formData.append('client_id', clientId.toString());
    }
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async analyze(documentId: number): Promise<DocumentAnalysis> {
    const response = await api.post(`/documents/${documentId}/analyze`);
    return response.data;
  },

  async list(): Promise<Document[]> {
    const response = await api.get('/documents/');
    return response.data;
  },

  async get(documentId: number): Promise<DocumentAnalysis> {
    const response = await api.get(`/documents/${documentId}`);
    return response.data;
  },

  async delete(documentId: number): Promise<void> {
    await api.delete(`/documents/${documentId}`);
  },
};

