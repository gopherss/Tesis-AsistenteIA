import { useEffect, useRef } from "react";
import { metricasService } from "../services/metricas.service";
import { useAuthStore } from "../store";

export const useTracking = () => {
  const sesionUsuarioId = useRef<number | null>(null);
  const clickCount = useRef(0);
  const startTime = useRef(Date.now());
  const { user } = useAuthStore();

  useEffect(() => {
    if (!user) return;

    metricasService.iniciarSesionUsuario().then((res) => {
      sesionUsuarioId.current = res.id;
    });

    const handleClick = () => {
      clickCount.current += 1;
    };

    document.addEventListener("click", handleClick);

    const interval = setInterval(() => {
      if (sesionUsuarioId.current && clickCount.current > 0) {
        metricasService.actualizarClicks(sesionUsuarioId.current, clickCount.current);
      }
    }, 30000);

    return () => {
      document.removeEventListener("click", handleClick);
      clearInterval(interval);

      if (sesionUsuarioId.current) {
        const duracion = Math.floor((Date.now() - startTime.current) / 1000);
        metricasService.actualizarClicks(sesionUsuarioId.current, clickCount.current);
        metricasService.finalizarSesionUsuario(sesionUsuarioId.current, duracion);
      }
    };
  }, [user?.id]);
};
