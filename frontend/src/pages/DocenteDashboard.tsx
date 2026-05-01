import { useEffect } from "react";
import { DashboardLayout, LoadingSpinner } from "../components";
import SesionCard from "../components/layout/SesionCard";
import { useAuthStore } from "../store/auth.store";
import { useSesionStore } from "../store/sesion.store";

const DocenteDashboard = () => {
  const { user } = useAuthStore();
  const {
    sesiones,
    listarSesiones,
    eliminarSesion,
    regenerarSesionIA,
    isLoading
  } = useSesionStore();

  useEffect(() => {
    listarSesiones();
  }, [listarSesiones]);

  if (sesiones.length < 0) return <h1 className="text-center text-red-500 ">No Hay Sesiones Creadas</h1>

  if (isLoading) return <LoadingSpinner fullScreen text="cargando" size="md" />

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-sm">
          <h1>{user?.nombre}</h1>
        </nav>
        <div className="mt-8">
          <h3 className="text-xl font-semibold">Mis sesiones</h3>
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
