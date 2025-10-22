import api from '../lib/api';

export interface KnowledgeBase {
  id: number;
  title: string;
  content: string;
  category?: string;
  source?: string;
  embedding_id?: string;
  created_at: string;
  updated_at: string;
}

export interface SearchResult {
  id: number;
  title: string;
  content: string;
  category?: string;
  score: number;
}

export interface RAGResponse {
  answer: string;
  sources: Array<{
    id: string;
    title: string;
    score: number;
    category?: string;
  }>;
  model: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export const knowledgeApi = {
  async create(data: {
    title: string;
    content: string;
    category?: string;
    source?: string;
  }): Promise<KnowledgeBase> {
    const response = await api.post('/knowledge/', data);
    return response.data;
  },

  async list(category?: string): Promise<KnowledgeBase[]> {
    const params = category ? { category } : {};
    const response = await api.get('/knowledge/', { params });
    return response.data;
  },

  async get(id: number): Promise<KnowledgeBase> {
    const response = await api.get(`/knowledge/${id}`);
    return response.data;
  },

  async search(query: string, limit: number = 5, category?: string): Promise<SearchResult[]> {
    const response = await api.post('/knowledge/search', {
      query,
      limit,
      category,
    });
    return response.data;
  },

  async ragQuery(query: string, limit: number = 3, category?: string): Promise<RAGResponse> {
    const response = await api.post('/knowledge/rag', {
      query,
      limit,
      category,
    });
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/knowledge/${id}`);
  },
};

