import api from '../api/axiosConfig';
import type { DashboardData, LoginCredentials, RegisterDocenteData, TokenResponse, Usuario } from '../types/auth.types';


export const authService = {
  // Login
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  // Registrar docente (solo directores)
  registerDocente: async (data: RegisterDocenteData): Promise<Usuario> => {
    const response = await api.post('/auth/register-docente', data);
    return response.data;
  },

  // Obtener dashboard (solo directores)
  getDashboard: async (): Promise<DashboardData> => {
    const response = await api.get('/auth/dashboard');
    return response.data;
  },

  // Obtener usuario actual
  getCurrentUser: async (): Promise<Usuario> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Logout
  logout: async (): Promise<{ mensaje: string }> => {
    const response = await api.post('/auth/logout');
    return response.data;
  }
};
