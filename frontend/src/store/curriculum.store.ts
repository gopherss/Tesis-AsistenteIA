import { create } from "zustand";
import { curriculumService } from "../services/curriculum.service";

interface CurriculumState {
  areas: any[];
  grados: any[];
  temas: any[];

  cargarAreas: () => Promise<void>;
  cargarGrados: () => Promise<void>;
  cargarTemas: (areaId: number, gradoId: number) => Promise<void>;
}

const useCurriculumStore = create<CurriculumState>((set) => ({
  areas: [],
  grados: [],
  temas: [],

  cargarAreas: async () => {
    const data = await curriculumService.getAreas();
    set({ areas: data });
  },

  cargarGrados: async () => {
    const data = await curriculumService.getGrados();
    set({ grados: data });
  },

  cargarTemas: async (areaId, gradoId) => {
    const data = await curriculumService.getTemas(areaId, gradoId);
    set({ temas: data });
  }
}));

export default useCurriculumStore;
