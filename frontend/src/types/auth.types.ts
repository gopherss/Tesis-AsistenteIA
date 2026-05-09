export interface LoginCredentials {
  email: string;
  password: string;
}

type UserRole = 'DIRECTOR' | 'DOCENTE';

export interface RegisterDocenteData {
  email: string;
  password: string;
  nombre: string;
  apellido: string;
  rol: UserRole;
}

export interface Usuario {
  id?: number;
  email: string;
  nombre: string;
  apellido: string;
  rol: UserRole;
  created_at?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface PaginatedDocentesResponse {
  total: number;
  page: number;
  limit: number;
  data: Usuario[];
}

export interface UpdateDocenteData {
  nombre: string;
  apellido: string;
  email: string;
}