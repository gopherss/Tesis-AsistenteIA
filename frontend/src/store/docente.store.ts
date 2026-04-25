import { create } from "zustand";
import { toast } from "sonner";
import {
  docenteService,
  type PlanificacionRequest,
  type AnalisisRequest
} from "../services/docente.service";

interface ChatMessage {
  tipo: "user" | "ia";
  texto: string;
}

interface DocenteState {
  loading: boolean;

  panel: any;
  obtenerPanel: () => Promise<void>;

  planificacion: any;
  obtenerPlanificacion: () => Promise<void>;

  sesiones: any[];
  obtenerSesiones: () => Promise<void>;

  planificacionIA: string;
  generarPlanificacionIA: (data: PlanificacionRequest) => Promise<void>;

  analisisIA: string;
  generarAnalisisIA: (data: AnalisisRequest) => Promise<void>;

  chat: ChatMessage[];
  iniciarChat: () => Promise<void>;
  enviarMensaje: (mensaje: string) => Promise<void>;

  limpiarResultados: () => void;
}

export const useDocenteStore = create<DocenteState>((set, get) => ({
  loading: false,
  panel: null,
  planificacion: null,
  sesiones: [],
  planificacionIA: "",
  analisisIA: "",
  chat: [],

  obtenerPanel: async () => {
    set({ loading: true });

    try {
      const data = await docenteService.getPanel();

      set({
        panel: data
      });
    } catch (error) {
      toast.error("Error cargando panel docente");
    } finally {
      set({ loading: false });
    }
  },

  obtenerPlanificacion: async () => {
    set({ loading: true });

    try {
      const data = await docenteService.getPlanificacion();

      set({
        planificacion: data
      });
    } catch (error) {
      toast.error("Error cargando planificación");
    } finally {
      set({ loading: false });
    }
  },

  obtenerSesiones: async () => {
    set({ loading: true });

    try {
      const data = await docenteService.getSesiones();

      set({
        sesiones: data.sesiones_activas || []
      });
    } catch (error) {
      toast.error("Error cargando sesiones");
    } finally {
      set({ loading: false });
    }
  },

  generarPlanificacionIA: async (data: PlanificacionRequest) => {
    set({ loading: true, planificacionIA: "" });

    try {
      const response = await docenteService.planificarSesion(data);

      set({
        planificacionIA: response.planificacion
      });

      toast.success("Sesión generada con IA");
    } catch (error) {
      toast.error("Error generando planificación");
    } finally {
      set({ loading: false });
    }
  },

  generarAnalisisIA: async (data: AnalisisRequest) => {
    set({ loading: true, analisisIA: "" });

    try {
      const response = await docenteService.analizarEstudiantes(data);

      set({
        analisisIA: response.analisis_ia
      });

      toast.success("Análisis completado");
    } catch (error) {
      toast.error("Error en análisis IA");
    } finally {
      set({ loading: false });
    }
  },

  iniciarChat: async () => {
    try {
      const response = await docenteService.iniciarChat();

      set({
        chat: [
          {
            tipo: "ia",
            texto: response.asistente
          }
        ]
      });
    } catch (error) {
      toast.error("No se pudo iniciar chat IA");
    }
  },

  enviarMensaje: async (mensaje: string) => {
    const historial = get().chat;

    set({
      chat: [
        ...historial,
        {
          tipo: "user",
          texto: mensaje
        }
      ]
    });

    try {
      const response = await docenteService.enviarMensaje(mensaje);

      set({
        chat: [
          ...get().chat,
          {
            tipo: "ia",
            texto: response.respuesta_ia
          }
        ]
      });
    } catch (error) {
      toast.error("Error enviando mensaje");
    }
  },

  limpiarResultados: () => {
    set({
      planificacionIA: "",
      analisisIA: "",
      chat: []
    });
  }
}));
