// ==============================================
// src/services/docente.service.ts
// ==============================================

import api from "../api/axiosConfig";

export interface PlanificacionRequest {
  nivel: string;
  grado: string;
  area: string;
  tema: string;
}

export interface AnalisisRequest {
  curso: string;
  total_estudiantes: number;
  promedio_general: number;
  asistencia: string;
}

export const docenteService = {
  // Panel principal
  getPanel: async () => {
    const response = await api.get("/docente/panel");
    return response.data;
  },

  // Planificación semanal
  getPlanificacion: async () => {
    const response = await api.get("/docente/planificacion");
    return response.data;
  },

  // Sesiones
  getSesiones: async () => {
    const response = await api.get("/docente/sesiones");
    return response.data;
  },

  // Chat IA iniciar
  iniciarChat: async () => {
    const response = await api.get("/docente/chat-iniciar");
    return response.data;
  },

  // Chat IA mensaje
  enviarMensaje: async (mensaje: string) => {
    const response = await api.post(
      "/docente/chat-mensaje",
      null,
      {
        params: { mensaje }
      }
    );
    return response.data;
  },

  // IA planificar sesión
  planificarSesion: async (data: PlanificacionRequest) => {
    const response = await api.post(
      "/docente/planificar-sesion",
      data
    );
    return response.data;
  },

  // IA analizar estudiantes
  analizarEstudiantes: async (data: AnalisisRequest) => {
    const response = await api.post(
      "/docente/analizar-estudiantes",
      data
    );
    return response.data;
  }
};