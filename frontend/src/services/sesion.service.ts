import api from "../api/axiosConfig";
import type {
  SesionCreate,
  SesionResponse,
} from "../types/sesion.types";

export const sesionService = {
  crearSesion: async (
    data: SesionCreate
  ): Promise<SesionResponse> => {
    const res = await api.post("/sesiones", data);
    return res.data;
  },

  listarSesiones: async (): Promise<SesionResponse[]> => {
    const res = await api.get("/sesiones");
    return res.data;
  },

  eliminarSesion: async (id: number): Promise<void> => {
    await api.delete(`/sesiones/${id}`);
  },

  regenerarSesionIA: async (
    id: number
  ): Promise<SesionResponse> => {
    const res = await api.put(
      `/sesiones/${id}/regenerar-ia`
    );
    return res.data;
  },

  descargarPdfSesion: async (id: number): Promise<void> => {
    const res = await api.get(
      `/sesiones/${id}/descargar-pdf`,
      {
        responseType: "blob",
      }
    );

    // Crear un blob y descargarlo
    const url = window.URL.createObjectURL(
      new Blob([res.data])
    );
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute(
      "download",
      `sesion_${id}.pdf`
    );
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(url);
  },
};

export const descargarPdfSesion = sesionService.descargarPdfSesion;