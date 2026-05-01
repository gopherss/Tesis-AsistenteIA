import api from "../api/axiosConfig";

export const curriculumService = {
    getAreas: async () => {
        const res = await api.get("/curriculum/areas");
        return res.data;
    },

    getGrados: async () => {
        const res = await api.get("/curriculum/grados");
        return res.data;
    },

    getTemas: async (areaId: number, gradoId: number) => {
        const res = await api.get(`/curriculum/temas?area_id=${areaId}&grado_id=${gradoId}`);
        return res.data;
    }
};
