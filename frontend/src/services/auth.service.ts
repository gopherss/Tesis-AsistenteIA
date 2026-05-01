import api from '../api/axiosConfig';
import type { LoginCredentials, RegisterDocenteData, TokenResponse, Usuario } from '../types/auth.types';

export const authService = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  registerDocente: async (data: RegisterDocenteData): Promise<Usuario> => {
    const response = await api.post('/auth/register-docente', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<Usuario> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  logout: async (): Promise<{ mensaje: string }> => {
    const response = await api.post('/auth/logout');
    return response.data;
  }
};
