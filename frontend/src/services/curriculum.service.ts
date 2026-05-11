import api from "../api/axiosConfig";
import type { Grado, Area, Competencia, Capacidad, Tema, Desempeno } from "../types/curriculum.types";

export const curriculumService = {
    getAreas: async (): Promise<Area[]> => {
        const res = await api.get("/curriculum/areas");
        return res.data;
    },

    getGrados: async (): Promise<Grado[]> => {
        const res = await api.get("/curriculum/grados");
        return res.data;
    },

    getTemas: async (areaId: number, gradoId: number): Promise<Tema[]> => {
        const res = await api.get(`/curriculum/temas?area_id=${areaId}&grado_id=${gradoId}`);
        return res.data;
    },

    getCompetencias: async (areaId: number): Promise<Competencia[]> => {
        const res = await api.get(`/curriculum/competencias?area_id=${areaId}`);
        return res.data;
    },

    getCapacidades: async (competenciaId: number): Promise<Capacidad[]> => {
        const res = await api.get(`/curriculum/capacidades?competencia_id=${competenciaId}`);
        return res.data;
    },

    getDesempenos: async (temaId: number): Promise<Desempeno[]> => {
        const res = await api.get(`/curriculum/desempenos?tema_id=${temaId}`);
        return res.data;
    },

    // ---- ADMIN CRUD ----

    // Grados
    adminGetGrados: async (): Promise<Grado[]> => {
        const res = await api.get("/curriculum/admin/grados");
        return res.data;
    },
    adminCreateGrado: async (data: { nombre: string; orden: number }): Promise<Grado> => {
        const res = await api.post("/curriculum/admin/grados", data);
        return res.data;
    },
    adminUpdateGrado: async (id: number, data: { nombre: string; orden: number }): Promise<Grado> => {
        const res = await api.put(`/curriculum/admin/grados/${id}`, data);
        return res.data;
    },
    adminDeleteGrado: async (id: number): Promise<void> => {
        await api.delete(`/curriculum/admin/grados/${id}`);
    },

    // Áreas
    adminGetAreas: async (): Promise<Area[]> => {
        const res = await api.get("/curriculum/admin/areas");
        return res.data;
    },
    adminCreateArea: async (data: { nombre: string }): Promise<Area> => {
        const res = await api.post("/curriculum/admin/areas", data);
        return res.data;
    },
    adminUpdateArea: async (id: number, data: { nombre: string }): Promise<Area> => {
        const res = await api.put(`/curriculum/admin/areas/${id}`, data);
        return res.data;
    },
    adminDeleteArea: async (id: number): Promise<void> => {
        await api.delete(`/curriculum/admin/areas/${id}`);
    },

    // Competencias
    adminGetCompetencias: async (areaId?: number): Promise<Competencia[]> => {
        const params = areaId ? `?area_id=${areaId}` : "";
        const res = await api.get(`/curriculum/admin/competencias${params}`);
        return res.data;
    },
    adminCreateCompetencia: async (data: { nombre: string; area_id: number }): Promise<Competencia> => {
        const res = await api.post("/curriculum/admin/competencias", data);
        return res.data;
    },
    adminUpdateCompetencia: async (id: number, data: { nombre: string; area_id: number }): Promise<Competencia> => {
        const res = await api.put(`/curriculum/admin/competencias/${id}`, data);
        return res.data;
    },
    adminDeleteCompetencia: async (id: number): Promise<void> => {
        await api.delete(`/curriculum/admin/competencias/${id}`);
    },

    // Capacidades
    adminGetCapacidades: async (competenciaId?: number): Promise<Capacidad[]> => {
        const params = competenciaId ? `?competencia_id=${competenciaId}` : "";
        const res = await api.get(`/curriculum/admin/capacidades${params}`);
        return res.data;
    },
    adminCreateCapacidad: async (data: { nombre: string; competencia_id: number }): Promise<Capacidad> => {
        const res = await api.post("/curriculum/admin/capacidades", data);
        return res.data;
    },
    adminUpdateCapacidad: async (id: number, data: { nombre: string; competencia_id: number }): Promise<Capacidad> => {
        const res = await api.put(`/curriculum/admin/capacidades/${id}`, data);
        return res.data;
    },
    adminDeleteCapacidad: async (id: number): Promise<void> => {
        await api.delete(`/curriculum/admin/capacidades/${id}`);
    },

    // Temas
    adminGetTemas: async (areaId?: number, gradoId?: number): Promise<Tema[]> => {
        const params = new URLSearchParams();
        if (areaId) params.append("area_id", String(areaId));
        if (gradoId) params.append("grado_id", String(gradoId));
        const res = await api.get(`/curriculum/admin/temas?${params.toString()}`);
        return res.data;
    },
    adminCreateTema: async (data: { nombre: string; area_id: number; grado_id: number }): Promise<Tema> => {
        const res = await api.post("/curriculum/admin/temas", data);
        return res.data;
    },
    adminUpdateTema: async (id: number, data: { nombre: string; area_id: number; grado_id: number }): Promise<Tema> => {
        const res = await api.put(`/curriculum/admin/temas/${id}`, data);
        return res.data;
    },
    adminDeleteTema: async (id: number): Promise<void> => {
        await api.delete(`/curriculum/admin/temas/${id}`);
    },

    // Desempeños
    adminGetDesempenos: async (temaId?: number): Promise<Desempeno[]> => {
        const params = temaId ? `?tema_id=${temaId}` : "";
        const res = await api.get(`/curriculum/admin/desempenos${params}`);
        return res.data;
    },
    adminCreateDesempeno: async (data: { descripcion: string; tema_id: number }): Promise<Desempeno> => {
        const res = await api.post("/curriculum/admin/desempenos", data);
        return res.data;
    },
    adminUpdateDesempeno: async (id: number, data: { descripcion: string; tema_id: number }): Promise<Desempeno> => {
        const res = await api.put(`/curriculum/admin/desempenos/${id}`, data);
        return res.data;
    },
    adminDeleteDesempeno: async (id: number): Promise<void> => {
        await api.delete(`/curriculum/admin/desempenos/${id}`);
    },
};
