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
};