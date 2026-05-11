export interface Grado {
  id: number;
  nombre: string;
  orden: number;
}

export interface Area {
  id: number;
  nombre: string;
  activo: boolean;
}

export interface Competencia {
  id: number;
  nombre: string;
  area_id: number;
}

export interface Capacidad {
  id: number;
  nombre: string;
  competencia_id: number;
}

export interface Tema {
  id: number;
  nombre: string;
  grado_id: number;
  area_id: number;
  activo: boolean;
}

export interface Desempeno {
  id: number;
  descripcion: string;
  tema_id: number;
}
