import { useNavigate } from "react-router-dom";
import { useCurriculumStore, useSesionStore } from "../store";
import { useEffect, useMemo, useRef, useState } from "react";
import { Button, DashboardLayout, Input, Select } from "../components";

const Sesiones = () => {
  const navigate = useNavigate();
  const { crearSesion, isLoading } = useSesionStore();

  const {
    areas,
    grados,
    temas,
    cargarAreas,
    cargarGrados,
    cargarTemas,
  } = useCurriculumStore();

  const isSubmittingRef = useRef(false);

  const [formData, setFormData] = useState({
    titulo: "",
    proposito: "",
    grado_id: "",
    area_id: "",
    tema: "",
    capacidades: "",
    desempeno: "",
    numero_ejercicios: 5,
    tiempo_sesion: 60,
  });

  useEffect(() => {
    cargarAreas();
    cargarGrados();
  }, []);

  useEffect(() => {
    if (formData.area_id && formData.grado_id) {
      cargarTemas(
        Number(formData.area_id),
        Number(formData.grado_id)
      );
    }
  }, [formData.area_id, formData.grado_id]);

  const selectedArea = useMemo(() => {
    return areas.find(
      (a: any) => String(a.id) === formData.area_id
    );
  }, [areas, formData.area_id]);

  const selectedGrado = useMemo(() => {
    return grados.find(
      (g: any) => String(g.id) === formData.grado_id
    );
  }, [grados, formData.grado_id]);

  const handleChange = (
    field: string,
    value: string | number
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleTemaChange = (value: string) => {
    const titulo = selectedArea
      ? `${selectedArea.nombre} - ${value}`
      : value;

    setFormData((prev) => ({
      ...prev,
      tema: value,
      titulo,
    }));
  };

  const resetForm = () => {
    setFormData({
      titulo: "",
      proposito: "",
      grado_id: "",
      area_id: "",
      tema: "",
      capacidades: "",
      desempeno: "",
      numero_ejercicios: 5,
      tiempo_sesion: 60,
    });
  };

  const handleSubmit = async (
    e: React.SyntheticEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    if (isSubmittingRef.current) return;
    isSubmittingRef.current = true;

    try {
      const ok = await crearSesion({
        titulo: formData.titulo,
        proposito: formData.proposito,
        grado: selectedGrado?.nombre || "",
        area: selectedArea?.nombre || "",
        tema: formData.tema,
        competencias: [],
        capacidades: formData.capacidades
          .split(",")
          .map((x) => x.trim())
          .filter(Boolean),
        desempeno: formData.desempeno
          .split(",")
          .map((x) => x.trim())
          .filter(Boolean),
        numero_ejercicios: Number(
          formData.numero_ejercicios
        ),
        tiempo_sesion: Number(
          formData.tiempo_sesion
        ),
      });

      if (ok) {
        resetForm();
        // Redirecciona al dashboard del docente después de crear la sesión
        navigate("/dashboard-docente");
      }
    } finally {
      isSubmittingRef.current = false;
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-5xl mx-auto px-4">
        <div className="mb-2">
          <h1 className="text-2xl font-bold text-slate-800">
            Crear Sesión Inteligente
          </h1>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-3xl shadow-xl border border-slate-200 p-4 sm:p-6 md:p-8 space-y-8"
        >
          {/* Resto de tu formulario igual... */}
          <section className="space-y-5">
            <h2 className="text-lg font-semibold text-slate-700 border-b pb-2">
              Información General
            </h2>
            <div className="grid md:grid-cols-2 gap-5">
              <Input
                label="Título"
                placeholder="Se genera automáticamente"
                value={formData.titulo}
                onChange={(e) => handleChange("titulo", e.target.value)}
                disabled
              />
              <Input
                label="Propósito"
                placeholder="¿Qué aprenderán hoy?"
                value={formData.proposito}
                onChange={(e) => handleChange("proposito", e.target.value)}
              />
            </div>
          </section>

          {/* Datos Curriculares */}
          <section className="space-y-5">
            <h2 className="text-lg font-semibold text-slate-700 border-b pb-2">
              Datos Curriculares
            </h2>

            <div className="grid md:grid-cols-2 gap-5">
              <Select
                label="Grado"
                value={formData.grado_id}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    grado_id: e.target.value,
                    tema: "",
                    titulo: "",
                  }))
                }
                options={grados.map((g: any) => ({
                  value: g.id,
                  label: g.nombre,
                }))}
                placeholder="Seleccione grado"
              />

              <Select
                label="Área"
                value={formData.area_id}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    area_id: e.target.value,
                    tema: "",
                    titulo: "",
                  }))
                }
                options={areas.map((a: any) => ({
                  value: a.id,
                  label: a.nombre,
                }))}
                placeholder="Seleccione área"
              />
            </div>

            <div>
              <Input
                label="Tema"
                placeholder="Escribe o selecciona sugerencia"
                value={formData.tema}
                onChange={(e) => handleTemaChange(e.target.value)}
              />

              {temas.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {temas.map((t: any) => (
                    <button
                      key={t.id}
                      type="button"
                      onClick={() => handleTemaChange(t.nombre)}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${formData.tema === t.nombre
                          ? "bg-blue-600 text-white"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                        }`}
                    >
                      {t.nombre}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </section>

          {/* Información Pedagógica */}
          <section className="space-y-5">
            <h2 className="text-lg font-semibold text-slate-700 border-b pb-2">
              Información Pedagógica
            </h2>

            <div className="grid md:grid-cols-2 gap-5">
              <Input
                label="Capacidades"
                placeholder="Separadas por coma"
                value={formData.capacidades}
                onChange={(e) => handleChange("capacidades", e.target.value)}
              />
              <Input
                label="Desempeño"
                placeholder="Separado por coma"
                value={formData.desempeno}
                onChange={(e) => handleChange("desempeno", e.target.value)}
              />
            </div>
          </section>

          {/* Configuración */}
          <section className="space-y-5">
            <h2 className="text-lg font-semibold text-slate-700 border-b pb-2">
              Configuración
            </h2>

            <div className="grid md:grid-cols-2 gap-5">
              <Input
                label="Ejercicios"
                type="number"
                min={1}
                value={formData.numero_ejercicios}
                onChange={(e) =>
                  handleChange("numero_ejercicios", Number(e.target.value))
                }
              />
              <Input
                label="Tiempo (min)"
                type="number"
                min={10}
                value={formData.tiempo_sesion}
                onChange={(e) => handleChange("tiempo_sesion", Number(e.target.value))}
              />
            </div>
          </section>

          <Button
            type="submit"
            disabled={isLoading}
            label={isLoading ? "Generando sesión..." : "Crear Sesión"}
            color="primary"
            full
          />          
        </form>
      </div>
    </DashboardLayout>
  );
};

export default Sesiones;