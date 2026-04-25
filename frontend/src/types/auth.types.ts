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

export interface DashboardData {
  mensaje: string;
  rol: UserRole;
  estadisticas: {
    total_docentes: number;
    total_cursos: number;
    docentes_activos: number;
    cursos_activos: number;
    asistencia_promedio: string;
    calificacion_promedio: number;
  };
  proximos_eventos: Array<{
    fecha: string;
    evento: string;
    hora: string;
  }>;
  notificaciones: string[];
}