import { useEffect, useState } from "react";
import { DashboardLayout, LoadingSpinner, SesionCard } from "../components";
import { useSesionStore } from "../store";
import { useTracking } from "../hooks/useTracking";
import { metricasService } from "../services/metricas.service";
import { toast } from "sonner";
import { MessageSquarePlus } from "lucide-react";

const DocenteDashboard = () => {
  const { sesiones, isLoading, listarSesiones, eliminarSesion, regenerarSesionIA } = useSesionStore();
  const [showEncuesta, setShowEncuesta] = useState(false);
  const [puntuacion, setPuntuacion] = useState(0);
  const [comentario, setComentario] = useState("");
  const [manualMinutos, setManualMinutos] = useState(0);
  const [manualTema, setManualTema] = useState("");

  useTracking();

  useEffect(() => {
    listarSesiones();
  }, []);

  const handleEncuesta = async () => {
    if (!puntuacion) return;
    try {
      await metricasService.crearEncuesta({ puntuacion, comentario });

      if (manualMinutos > 0) {
        await metricasService.registrarSinPlataforma({
          tiempo_total_segundos: manualMinutos * 60,
          tema: manualTema,
        });
      }

      toast.success("Gracias por tu feedback");
      setShowEncuesta(false);
      setPuntuacion(0);
      setComentario("");
      setManualMinutos(0);
      setManualTema("");
    } catch {
      toast.error("Error al enviar");
    }
  };

  if (isLoading)
    return (
      <DashboardLayout>
        <LoadingSpinner fullScreen text="cargando" size="sm" />
      </DashboardLayout>
    );

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-100">
        <div className="mt-8">
          <h3 className="text-xl font-semibold text-red-400 m-2">Mis sesiones</h3>
          <div className="columns-1 md:columns-2 gap-6 mt-4 space-y-6">
            {sesiones.map((s) => (
              <SesionCard key={s.id} sesion={s} onDelete={eliminarSesion} onRegenerar={regenerarSesionIA} />
            ))}
          </div>
        </div>
      </div>

      <button
        onClick={() => setShowEncuesta(true)}
        className="fixed bottom-6 right-6 z-50 bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-lg transition hover:scale-105"
        title="Encuesta de satisfacción"
      >
        <MessageSquarePlus size={24} />
      </button>

      {showEncuesta && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4 shadow-2xl">
            <h3 className="text-lg font-bold mb-4">Encuesta de Satisfacción</h3>

            <p className="text-sm text-gray-500 mb-3">¿Cómo calificas la plataforma?</p>
            <div className="flex gap-2 mb-4">
              {[1, 2, 3, 4, 5].map((n) => (
                <button
                  key={n}
                  onClick={() => setPuntuacion(n)}
                  className={`w-10 h-10 rounded-full text-lg font-bold transition ${
                    puntuacion >= n ? "bg-yellow-400 text-white" : "bg-gray-200 text-gray-500"
                  }`}
                >
                  {n}
                </button>
              ))}
            </div>

            <textarea
              placeholder="Comentario (opcional)"
              value={comentario}
              onChange={(e) => setComentario(e.target.value)}
              className="w-full border rounded-lg p-3 text-sm mb-4 resize-none h-20"
            />

            <hr className="my-4" />
            <p className="text-sm text-gray-500 mb-3">¿Cuánto tiempo te tomó crear una sesión sin la plataforma?</p>
            <div className="space-y-3 mb-4">
              <input
                type="text"
                placeholder="Tema (opcional)"
                value={manualTema}
                onChange={(e) => setManualTema(e.target.value)}
                className="w-full border rounded-lg p-3 text-sm"
              />
              <input
                type="number"
                min={1}
                placeholder="Minutos invertidos"
                value={manualMinutos || ""}
                onChange={(e) => setManualMinutos(Number(e.target.value))}
                className="w-full border rounded-lg p-3 text-sm"
              />
            </div>

            <div className="flex gap-2 justify-end">
              <button onClick={() => setShowEncuesta(false)} className="px-4 py-2 bg-gray-200 rounded-lg text-sm">
                Cancelar
              </button>
              <button
                onClick={handleEncuesta}
                disabled={!puntuacion}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm disabled:bg-gray-400"
              >
                Enviar
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
};

export default DocenteDashboard;
