import { useEffect } from "react";
import { DashboardLayout, LoadingSpinner, SesionCard } from "../components";
import { useSesionStore } from "../store";

const DocenteDashboard = () => {
  const {
    sesiones,
    isLoading,
    listarSesiones,
    eliminarSesion,
    regenerarSesionIA,
  } = useSesionStore();

  useEffect(() => {
    listarSesiones();
  }, []);

  if (isLoading) return (
    <DashboardLayout>
      <LoadingSpinner fullScreen text="cargando" size="sm" />
    </DashboardLayout>
  )

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-100">
        <div className="mt-8">
          <h3 className="text-xl font-semibold text-red-400 m-2">Mis sesiones</h3>
          <div className="columns-1 md:columns-2 gap-6 mt-4 space-y-6">
            {sesiones.map((s) => (
              <SesionCard
                key={s.id}
                sesion={s}
                onDelete={eliminarSesion}
                onRegenerar={regenerarSesionIA}
              />
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DocenteDashboard;
