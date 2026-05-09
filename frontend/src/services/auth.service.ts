import api from '../api/axiosConfig';
import type {
  LoginCredentials,
  RegisterDocenteData,
  TokenResponse,
  Usuario,
  PaginatedDocentesResponse,
  UpdateDocenteData
} from '../types/auth.types';

export const authService = {

  login: async (
    credentials: LoginCredentials
  ): Promise<TokenResponse> => {

    const response = await api.post(
      '/auth/login',
      credentials
    );

    return response.data;
  },

  registerDocente: async (
    data: RegisterDocenteData
  ): Promise<Usuario> => {

    const response = await api.post(
      '/auth/register-docente',
      data
    );

    return response.data;
  },

  getDocentes: async (
    page = 1,
    limit = 5
  ): Promise<PaginatedDocentesResponse> => {

    const response = await api.get(
      `/auth/docentes?page=${page}&limit=${limit}`
    );

    return response.data;
  },

  updateDocente: async (
    id: number,
    data: UpdateDocenteData
  ): Promise<Usuario> => {

    const response = await api.put(
      `/auth/docentes/${id}`,
      data
    );

    return response.data;
  },

  deleteDocente: async (
    id: number
  ): Promise<void> => {

    await api.delete(`/auth/docentes/${id}`);
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