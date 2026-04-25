import { useEffect, useState } from 'react';
import { DashboardLayout, LoadingSpinner } from '../components';
import { authService } from '../services/auth.service';
import type { DashboardData } from '../types/auth.types';

const DirectorDashboard = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  
  const fetchDashboard = async () => {
    try {
      const data = await authService.getDashboard();
      setDashboardData(data);
    } catch (error) {
      console.error( `Error fetching dashboard:error ${error}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);


  if (loading) {
    return (
      <LoadingSpinner size='lg' text='cargando dashboard...' />
    );
  }

  return (
    <DashboardLayout>

      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {/* Estadísticas */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Total Docentes</h3>
              <p className="text-3xl font-bold text-indigo-600">
                {dashboardData?.estadisticas.total_docentes}
              </p>
              <p className="text-sm text-gray-500">
                Activos: {dashboardData?.estadisticas.docentes_activos}
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Total Cursos</h3>
              <p className="text-3xl font-bold text-indigo-600">
                {dashboardData?.estadisticas.total_cursos}
              </p>
              <p className="text-sm text-gray-500">
                Activos: {dashboardData?.estadisticas.cursos_activos}
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-medium text-gray-900">Métricas</h3>
              <p className="text-2xl font-bold text-indigo-600">
                {dashboardData?.estadisticas.asistencia_promedio}
              </p>
              <p className="text-sm text-gray-500">
                Calificación: {dashboardData?.estadisticas.calificacion_promedio}
              </p>
            </div>
          </div>

          {/* Eventos y Notificaciones */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium mb-4">Próximos Eventos</h3>
              <div className="space-y-3">
                {dashboardData?.proximos_eventos.map((evento, idx) => (
                  <div key={idx} className="border-l-4 border-indigo-500 pl-3">
                    <p className="font-medium">{evento.evento}</p>
                    <p className="text-sm text-gray-500">
                      {evento.fecha} - {evento.hora}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium mb-4">Notificaciones</h3>
              <ul className="space-y-2">
                {dashboardData?.notificaciones.map((notif, idx) => (
                  <li key={idx} className="text-gray-600">• {notif}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DirectorDashboard;
