import { useEffect, useState } from "react";
import { DashboardLayout, LoadingSpinner } from "../components";
import { useAuthStore } from "../store";
import { metricasService } from "../services/metricas.service";
import type { Estadisticas } from "../types/metricas.types";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Legend } from "recharts";

const COLORS = ["#6366f1", "#f97316", "#22c55e", "#ef4444", "#eab308"];

interface BarraProps<T> {
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  payload?: T;
}

const BarraColoreada = <T extends { fill: string }>({
  x,
  y,
  width,
  height,
  payload,
}: BarraProps<T>) => {
  if (!payload || !width || !height) return null;
  return (
    <rect
      x={x}
      y={y}
      width={width}
      height={height}
      fill={payload.fill}
      rx={6}
      ry={6}
    />
  );
};

const DirectorDashboard = () => {
  const { user } = useAuthStore();
  const [data, setData] = useState<Estadisticas | null>(null);

  useEffect(() => {
    metricasService.getEstadisticas().then(setData).catch(() => {});
  }, []);

  const comparacion = data
    ? [
        { name: "Con plataforma", segundos: data.tiempo_promedio_con_plataforma },
        { name: "Sin plataforma", segundos: data.tiempo_promedio_sin_plataforma },
      ]
    : [];

  const sesionesPie = data
    ? [
        { name: "Con plataforma", value: data.total_sesiones_con_plataforma, fill: COLORS[0] },
        { name: "Sin plataforma", value: data.total_sesiones_sin_plataforma, fill: COLORS[1] },
      ]
    : [];

  const sesionesPorDocente = data?.sesiones_por_docente.map((d, i) => ({
    ...d,
    nombre: d.nombre.split(" ")[0],
    nombreCompleto: d.nombre,
    fill: COLORS[i % COLORS.length],
  })) ?? [];

  return (
    <DashboardLayout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Panel del Director</h1>
        <p className="text-sm text-gray-500 mt-1">Bienvenido, {user?.nombre}</p>
      </div>

      {!data ? (
        <LoadingSpinner fullScreen size="lg" text="Cargando..."/>
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card label="Docentes" value={data.total_docentes} />
            <Card label="Sesiones con IA" value={data.total_sesiones_con_plataforma} />
            <Card label="Sesiones manuales" value={data.total_sesiones_sin_plataforma} />
            <Card label="Encuestas" value={data.total_encuestas} />
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="font-semibold text-slate-700 mb-4">Sesiones por docente</h3>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={sesionesPorDocente}>
                <XAxis dataKey="nombre" />
                <YAxis />
                <Tooltip
                  formatter={(value, _name, item) => [value, `Sesiones de ${item.payload?.nombreCompleto}`]}
                  labelStyle={{ display: "none" }}
                />
                <Bar dataKey="total" shape={<BarraColoreada />} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="font-semibold text-slate-700 mb-4">Tiempo promedio de creación (segundos)</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={comparacion}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="segundos" fill="#6366f1" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="font-semibold text-slate-700 mb-4">Sesiones: con IA vs manual</h3>
              <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                  <Pie data={sesionesPie} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label />
                  <Legend />
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="font-semibold text-slate-700 mb-4">Métricas clave</h3>
              <div className="space-y-3">
                <MetricRow label="Tiempo promedio API DeepSeek" value={`${data.tiempo_promedio_api}s`} />
                <MetricRow label="Tiempo total con plataforma" value={`${data.tiempo_promedio_con_plataforma}s`} />
                <MetricRow label="Tiempo total sin plataforma" value={`${data.tiempo_promedio_sin_plataforma}s`} />
                <MetricRow label="Clicks promedio por sesión" value={`${data.clicks_promedio_por_sesion}`} />
                <MetricRow label="Satisfacción promedio" value={`${data.satisfaccion_promedio} / 5`} />
              </div>
            </div>

            {data.satisfaccion_reciente.length > 0 && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="font-semibold text-slate-700 mb-4">Últimas encuestas</h3>
                <div className="space-y-2">
                  {data.satisfaccion_reciente.map((e, i) => (
                    <div key={i} className="flex items-center gap-3 bg-gray-50 rounded-lg p-3 text-sm">
                      <span className="font-medium text-indigo-600 min-w-[140px]">{e.docente}</span>
                      <span className="text-yellow-500 font-bold">{e.puntuacion}/5</span>
                      <span className="text-gray-500 truncate">{e.comentario || "—"}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </DashboardLayout>
  );
};

const Card = ({ label, value }: { label: string; value: number }) => (
  <div className="bg-white rounded-lg shadow p-5">
    <p className="text-sm text-gray-500">{label}</p>
    <p className="text-3xl font-bold text-indigo-600 mt-1">{value}</p>
  </div>
);

const MetricRow = ({ label, value }: { label: string; value: string }) => (
  <div className="flex justify-between items-center border-b pb-2">
    <span className="text-sm text-gray-600">{label}</span>
    <span className="font-semibold text-slate-800">{value}</span>
  </div>
);

export default DirectorDashboard;
