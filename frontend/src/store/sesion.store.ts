import { create } from "zustand";
import { toast } from "sonner";
import { sesionService } from "../services/sesion.service";
import type {
  SesionCreate,
  SesionUpdateData,
  SesionResponse,
} from "../types/sesion.types";

interface SesionState {
  sesiones: SesionResponse[];
  isLoading: boolean;

  listarSesiones: () => Promise<void>;
  crearSesion: (data: SesionCreate) => Promise<boolean>;

  eliminarSesion: (id: number) => Promise<void>;
  regenerarSesionIA: (id: number) => Promise<void>;
  actualizarSesion: (id: number, data: SesionUpdateData) => Promise<boolean>;
}

const useSesionStore =
  create<SesionState>((set) => ({
    sesiones: [],
    isLoading: false,

    listarSesiones: async () => {
      set({ isLoading: true });

      try {
        const sesiones =
          await sesionService.listarSesiones();

        set({
          sesiones,
          isLoading: false,
        });
      } catch {
        toast.error("Error al cargar sesiones");
        set({ isLoading: false });
      }
    },

    crearSesion: async (data) => {
      set({ isLoading: true });

      try {
        const nueva =
          await sesionService.crearSesion(data);

        set((state) => ({
          sesiones: [nueva, ...state.sesiones],
          isLoading: false,
        }));

        toast.success("Sesión creada");
        return true;
      } catch (error: any) {
        const detail =
          error.response?.data?.detail;

        const message =
          typeof detail === "string"
            ? detail
            : detail?.mensaje ||
            "Error al crear sesión";

        toast.error(message);

        set({ isLoading: false });
        return false;
      }
    },

    eliminarSesion: async (id) => {
      try {
        await sesionService.eliminarSesion(id);

        set((state) => ({
          sesiones: state.sesiones.filter(
            (s) => s.id !== id
          ),
        }));

        toast.success("Sesión eliminada");
      } catch {
        toast.error("No se pudo eliminar");
      }
    },

    actualizarSesion: async (id, data) => {
      try {
        const actualizada = await sesionService.actualizarSesion(id, data);
        set((state) => ({
          sesiones: state.sesiones.map((s) => (s.id === id ? actualizada : s)),
        }));
        toast.success("Sesión actualizada");
        return true;
      } catch (error: any) {
        toast.error(error.response?.data?.detail || "Error al actualizar");
        return false;
      }
    },

    regenerarSesionIA: async (id) => {
      try {
        toast.loading("Regenerando IA...", {
          id: "regen",
        });

        const actualizada =
          await sesionService.regenerarSesionIA(
            id
          );

        set((state) => ({
          sesiones: state.sesiones.map((s) =>
            s.id === id ? actualizada : s
          ),
        }));

        toast.success("IA regenerada", {
          id: "regen",
        });
      } catch {
        toast.error("No se pudo regenerar", {
          id: "regen",
        });
      }
    },
  }));

export default useSesionStore;
