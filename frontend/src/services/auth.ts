import api from '../lib/api'

export interface LoginData {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
}

export const authApi = {
  login: async (data: LoginData) => {
    const response = await api.post('/auth/login', data)
    return response.data
  },
  
  register: async (data: RegisterData) => {
    const response = await api.post('/auth/register', data)
    return response.data
  },
  
  getMe: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

