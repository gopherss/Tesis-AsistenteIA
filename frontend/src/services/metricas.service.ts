import api from "../api/axiosConfig";
import type { Estadisticas } from "../types/metricas.types";

export const metricasService = {
  iniciarSesionUsuario: async (): Promise<{ id: number; inicio: string }> => {
    const res = await api.post("/metricas/iniciar-sesion");
    return res.data;
  },

  actualizarClicks: async (sesionUsuarioId: number, clicks: number): Promise<void> => {
    await api.put(`/metricas/sesion/${sesionUsuarioId}/clicks`, { clicks });
  },

  finalizarSesionUsuario: async (sesionUsuarioId: number, duracion_segundos: number): Promise<void> => {
    await api.put(`/metricas/sesion/${sesionUsuarioId}/finalizar`, { duracion_segundos });
  },

  crearEncuesta: async (data: { puntuacion: number; comentario?: string; sesion_id?: number }): Promise<void> => {
    await api.post("/metricas/encuesta", data);
  },

  registrarSinPlataforma: async (data: { tiempo_total_segundos: number; tema?: string; area?: string; grado?: string }): Promise<void> => {
    await api.post("/metricas/registrar-sin-plataforma", data);
  },

  getEstadisticas: async (): Promise<Estadisticas> => {
    const res = await api.get("/metricas/estadisticas");
    return res.data;
  },
};
