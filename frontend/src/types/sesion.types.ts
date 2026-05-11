export interface SesionCreate {
  titulo: string;
  proposito: string;
  grado: string;
  area: string;
  tema: string;
  competencias: string[];
  capacidades: string[];
  desempeno: string[];
  numero_ejercicios: number;
  tiempo_sesion: number;
  tiempo_total_segundos?: number;
}

export interface SesionUpdateData {
  titulo: string;
  proposito: string;
  grado: string;
  area: string;
  tema: string;
  competencias: string[];
  capacidades: string[];
  desempeno: string[];
  numero_ejercicios: number;
  tiempo_sesion: number;
}

export interface SesionResponse extends SesionCreate {
  id: number;
  contenido_ia?: string;
  usuario_id: number;
}
