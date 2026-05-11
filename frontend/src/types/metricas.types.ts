export interface Estadisticas {
  total_docentes: number;
  total_sesiones_con_plataforma: number;
  total_sesiones_sin_plataforma: number;
  tiempo_promedio_con_plataforma: number;
  tiempo_promedio_sin_plataforma: number;
  tiempo_promedio_api: number;
  clicks_promedio_por_sesion: number;
  satisfaccion_promedio: number;
  total_encuestas: number;
  sesiones_por_docente: { nombre: string; total: number }[];
  satisfaccion_reciente: {
    docente: string;
    puntuacion: number;
    comentario: string;
    fecha: string;
  }[];
}
