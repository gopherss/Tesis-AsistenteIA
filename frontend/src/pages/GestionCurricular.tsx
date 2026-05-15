import { useEffect, useState } from "react";
import { Button, DashboardLayout, Input, Select } from "../components";
import { curriculumService } from "../services/curriculum.service";
import { toast } from "sonner";
import { validarCampoVacio } from "../utils/validators";
import type { Grado, Area, Competencia, Capacidad, Tema, Desempeno } from "../types/curriculum.types";

type EntityType = "grados" | "areas" | "competencias" | "capacidades" | "temas" | "desempenos";

interface Option {
  value: string | number;
  label: string;
}

const ENTITIES: { value: EntityType; label: string }[] = [
  { value: "grados", label: "Grados" },
  { value: "areas", label: "Áreas" },
  { value: "competencias", label: "Competencias" },
  { value: "capacidades", label: "Capacidades" },
  { value: "temas", label: "Temas" },
  { value: "desempenos", label: "Desempeños" },
];

const initialForm = {
  nombre: "",
  orden: 0,
  area_id: "",
  grado_id: "",
  competencia_id: "",
  tema_id: "",
  descripcion: "",
};

const GestionCurricular = () => {
  const [entityType, setEntityType] = useState<EntityType>("grados");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState({ ...initialForm });
  const [errores, setErrores] = useState<Record<string, string>>({});

  // Lists
  const [grados, setGrados] = useState<Grado[]>([]);
  const [areas, setAreas] = useState<Area[]>([]);
  const [competencias, setCompetencias] = useState<Competencia[]>([]);
  const [capacidades, setCapacidades] = useState<Capacidad[]>([]);
  const [temas, setTemas] = useState<Tema[]>([]);
  const [desempenos, setDesempenos] = useState<Desempeno[]>([]);

  // Filter states for nested selects
  const [filterAreaId, setFilterAreaId] = useState("");
  const [filterCompetenciaId, setFilterCompetenciaId] = useState("");
  const [filterGradoId, setFilterGradoId] = useState("");
  const [filterTemaId, setFilterTemaId] = useState("");

  const loadAll = async () => {
    try {
      const [g, a] = await Promise.all([
        curriculumService.adminGetGrados(),
        curriculumService.adminGetAreas(),
      ]);
      setGrados(g);
      setAreas(a);
    } catch {
      toast.error("Error cargando datos");
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  // Load entity-specific lists when entity type or filters change
  useEffect(() => {
    if (entityType === "competencias") {
      curriculumService.adminGetCompetencias(filterAreaId ? Number(filterAreaId) : undefined).then(setCompetencias).catch(() => {});
    }
  }, [entityType, filterAreaId]);

  useEffect(() => {
    if (entityType === "capacidades") {
      curriculumService.adminGetCapacidades(filterCompetenciaId ? Number(filterCompetenciaId) : undefined).then(setCapacidades).catch(() => {});
    }
  }, [entityType, filterCompetenciaId]);

  useEffect(() => {
    if (entityType === "temas") {
      curriculumService.adminGetTemas(filterAreaId ? Number(filterAreaId) : undefined, filterGradoId ? Number(filterGradoId) : undefined).then(setTemas).catch(() => {});
    }
  }, [entityType, filterAreaId, filterGradoId]);

  useEffect(() => {
    if (entityType === "desempenos") {
      curriculumService.adminGetDesempenos(filterTemaId ? Number(filterTemaId) : undefined).then(setDesempenos).catch(() => {});
    }
  }, [entityType, filterTemaId]);

  // ---- Validation ----

  const validar = (): boolean => {
    const errs: Record<string, string> = {};
    if (entityType === "grados") {
      const n = validarCampoVacio(form.nombre, "El nombre");
      if (n) errs.nombre = n;
    } else if (entityType === "areas") {
      const n = validarCampoVacio(form.nombre, "El nombre");
      if (n) errs.nombre = n;
    } else if (entityType === "competencias") {
      const a = validarCampoVacio(form.area_id, "El área");
      if (a) errs.area_id = a;
      const n = validarCampoVacio(form.nombre, "El nombre");
      if (n) errs.nombre = n;
    } else if (entityType === "capacidades") {
      const c = validarCampoVacio(form.competencia_id, "La competencia");
      if (c) errs.competencia_id = c;
      const n = validarCampoVacio(form.nombre, "El nombre");
      if (n) errs.nombre = n;
    } else if (entityType === "temas") {
      const a = validarCampoVacio(form.area_id, "El área");
      if (a) errs.area_id = a;
      const g = validarCampoVacio(form.grado_id, "El grado");
      if (g) errs.grado_id = g;
      const n = validarCampoVacio(form.nombre, "El nombre");
      if (n) errs.nombre = n;
    } else if (entityType === "desempenos") {
      const t = validarCampoVacio(form.tema_id, "El tema");
      if (t) errs.tema_id = t;
      const d = validarCampoVacio(form.descripcion, "La descripción");
      if (d) errs.descripcion = d;
    }
    setErrores(errs);
    return Object.keys(errs).length === 0;
  };

  // ---- Form handlers ----

  const resetForm = () => {
    setForm({ ...initialForm });
    setEditingId(null);
    setErrores({});
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validar()) return;
    try {
      if (entityType === "grados") {
        if (editingId) {
          await curriculumService.adminUpdateGrado(editingId, { nombre: form.nombre, orden: Number(form.orden) });
          toast.success("Grado actualizado");
        } else {
          await curriculumService.adminCreateGrado({ nombre: form.nombre, orden: Number(form.orden) });
          toast.success("Grado creado");
        }
        setGrados(await curriculumService.adminGetGrados());
      } else if (entityType === "areas") {
        if (editingId) {
          await curriculumService.adminUpdateArea(editingId, { nombre: form.nombre });
          toast.success("Área actualizada");
        } else {
          await curriculumService.adminCreateArea({ nombre: form.nombre });
          toast.success("Área creada");
        }
        setAreas(await curriculumService.adminGetAreas());
      } else if (entityType === "competencias") {
        const payload = { nombre: form.nombre, area_id: Number(form.area_id) };
        if (editingId) {
          await curriculumService.adminUpdateCompetencia(editingId, payload);
          toast.success("Competencia actualizada");
        } else {
          await curriculumService.adminCreateCompetencia(payload);
          toast.success("Competencia creada");
        }
        setCompetencias(await curriculumService.adminGetCompetencias(filterAreaId ? Number(filterAreaId) : undefined));
      } else if (entityType === "capacidades") {
        const payload = { nombre: form.nombre, competencia_id: Number(form.competencia_id) };
        if (editingId) {
          await curriculumService.adminUpdateCapacidad(editingId, payload);
          toast.success("Capacidad actualizada");
        } else {
          await curriculumService.adminCreateCapacidad(payload);
          toast.success("Capacidad creada");
        }
        setCapacidades(await curriculumService.adminGetCapacidades(filterCompetenciaId ? Number(filterCompetenciaId) : undefined));
      } else if (entityType === "temas") {
        const payload = { nombre: form.nombre, area_id: Number(form.area_id), grado_id: Number(form.grado_id) };
        if (editingId) {
          await curriculumService.adminUpdateTema(editingId, payload);
          toast.success("Tema actualizado");
        } else {
          await curriculumService.adminCreateTema(payload);
          toast.success("Tema creado");
        }
        setTemas(await curriculumService.adminGetTemas(filterAreaId ? Number(filterAreaId) : undefined, filterGradoId ? Number(filterGradoId) : undefined));
      } else if (entityType === "desempenos") {
        const payload = { descripcion: form.descripcion, tema_id: Number(form.tema_id) };
        if (editingId) {
          await curriculumService.adminUpdateDesempeno(editingId, payload);
          toast.success("Desempeño actualizado");
        } else {
          await curriculumService.adminCreateDesempeno(payload);
          toast.success("Desempeño creado");
        }
        setDesempenos(await curriculumService.adminGetDesempenos(filterTemaId ? Number(filterTemaId) : undefined));
      }
      resetForm();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Error al guardar");
    }
  };

  const handleEdit = (item: any) => {
    setEditingId(item.id);
    setErrores({});
    if (entityType === "grados") {
      setForm({ ...initialForm, nombre: item.nombre, orden: item.orden });
    } else if (entityType === "areas") {
      setForm({ ...initialForm, nombre: item.nombre });
    } else if (entityType === "competencias") {
      setForm({ ...initialForm, nombre: item.nombre, area_id: String(item.area_id) });
    } else if (entityType === "capacidades") {
      setForm({ ...initialForm, nombre: item.nombre, competencia_id: String(item.competencia_id) });
    } else if (entityType === "temas") {
      setForm({ ...initialForm, nombre: item.nombre, area_id: String(item.area_id), grado_id: String(item.grado_id) });
    } else if (entityType === "desempenos") {
      setForm({ ...initialForm, descripcion: item.descripcion, tema_id: String(item.tema_id) });
    }
  };

  const handleDelete = async (id: number) => {
    try {
      if (entityType === "grados") {
        await curriculumService.adminDeleteGrado(id);
        setGrados(await curriculumService.adminGetGrados());
      } else if (entityType === "areas") {
        await curriculumService.adminDeleteArea(id);
        setAreas(await curriculumService.adminGetAreas());
      } else if (entityType === "competencias") {
        await curriculumService.adminDeleteCompetencia(id);
        setCompetencias(await curriculumService.adminGetCompetencias(filterAreaId ? Number(filterAreaId) : undefined));
      } else if (entityType === "capacidades") {
        await curriculumService.adminDeleteCapacidad(id);
        setCapacidades(await curriculumService.adminGetCapacidades(filterCompetenciaId ? Number(filterCompetenciaId) : undefined));
      } else if (entityType === "temas") {
        await curriculumService.adminDeleteTema(id);
        setTemas(await curriculumService.adminGetTemas(filterAreaId ? Number(filterAreaId) : undefined, filterGradoId ? Number(filterGradoId) : undefined));
      } else if (entityType === "desempenos") {
        await curriculumService.adminDeleteDesempeno(id);
        setDesempenos(await curriculumService.adminGetDesempenos(filterTemaId ? Number(filterTemaId) : undefined));
      }
      toast.success("Eliminado correctamente");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Error al eliminar");
    }
  };

  const areasOptions: Option[] = areas.map((a) => ({ value: a.id, label: a.nombre }));
  const gradosOptions: Option[] = grados.map((g) => ({ value: g.id, label: g.nombre }));
  const competenciasOptions: Option[] = competencias.map((c) => ({ value: c.id, label: c.nombre }));
  const temasOptions: Option[] = temas.map((t) => ({ value: t.id, label: t.nombre }));

  const handleFormChange = (field: string, value: any) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setErrores((prev) => {
      if (prev[field]) {
        const copy = { ...prev };
        delete copy[field];
        return copy;
      }
      return prev;
    });
  };

  const renderForm = () => {
    return (
      <form onSubmit={handleSubmit} className="space-y-4">
        {entityType === "grados" && (
          <>
            <Input
              label="Nombre del grado"
              value={form.nombre}
              onChange={(e) => handleFormChange("nombre", e.target.value)}
              error={errores.nombre}
            />
            <Input
              label="Orden"
              type="number"
              value={form.orden}
              onChange={(e) => handleFormChange("orden", Number(e.target.value))}
            />
          </>
        )}

        {entityType === "areas" && (
          <Input
            label="Nombre del área"
            value={form.nombre}
            onChange={(e) => handleFormChange("nombre", e.target.value)}
            error={errores.nombre}
          />
        )}

        {entityType === "competencias" && (
          <>
            <Select
              label="Área"
              value={form.area_id}
              onChange={(e) => handleFormChange("area_id", e.target.value)}
              options={areasOptions}
              placeholder="Seleccione área"
              error={errores.area_id}
            />
            <Input
              label="Nombre de la competencia"
              value={form.nombre}
              onChange={(e) => handleFormChange("nombre", e.target.value)}
              error={errores.nombre}
            />
          </>
        )}

        {entityType === "capacidades" && (
          <>
            <Select
              label="Área"
              value={filterAreaId}
              onChange={(e) => { setFilterAreaId(e.target.value); setFilterCompetenciaId(""); }}
              options={areasOptions}
              placeholder="Filtrar por área"
            />
            <Select
              label="Competencia"
              value={form.competencia_id}
              onChange={(e) => handleFormChange("competencia_id", e.target.value)}
              options={competenciasOptions}
              placeholder="Seleccione competencia"
              error={errores.competencia_id}
            />
            <Input
              label="Nombre de la capacidad"
              value={form.nombre}
              onChange={(e) => handleFormChange("nombre", e.target.value)}
              error={errores.nombre}
            />
          </>
        )}

        {entityType === "temas" && (
          <>
            <div className="grid grid-cols-2 gap-3">
              <Select
                label="Área"
                value={form.area_id}
                onChange={(e) => handleFormChange("area_id", e.target.value)}
                options={areasOptions}
                placeholder="Seleccione área"
                error={errores.area_id}
              />
              <Select
                label="Grado"
                value={form.grado_id}
                onChange={(e) => handleFormChange("grado_id", e.target.value)}
                options={gradosOptions}
                placeholder="Seleccione grado"
                error={errores.grado_id}
              />
            </div>
            <Input
              label="Nombre del tema"
              value={form.nombre}
              onChange={(e) => handleFormChange("nombre", e.target.value)}
              error={errores.nombre}
            />
          </>
        )}

        {entityType === "desempenos" && (
          <>
            <div className="grid grid-cols-2 gap-3">
              <Select label="Área" value={filterAreaId} onChange={(e) => { setFilterAreaId(e.target.value); setFilterTemaId(""); }} options={areasOptions} placeholder="Filtrar por área" />
              <Select label="Grado" value={filterGradoId} onChange={(e) => { setFilterGradoId(e.target.value); setFilterTemaId(""); }} options={gradosOptions} placeholder="Filtrar por grado" />
            </div>
            <Select
              label="Tema"
              value={form.tema_id}
              onChange={(e) => handleFormChange("tema_id", e.target.value)}
              options={temasOptions}
              placeholder="Seleccione tema"
              error={errores.tema_id}
            />
            <Input
              label="Descripción del desempeño"
              value={form.descripcion}
              onChange={(e) => handleFormChange("descripcion", e.target.value)}
              error={errores.descripcion}
            />
          </>
        )}

        <div className="flex gap-2">
          <Button type="submit" label={editingId ? "Actualizar" : "Crear"} color="primary" />
          {editingId && <Button type="button" label="Cancelar" color="secondary" onClick={resetForm} />}
        </div>
      </form>
    );
  };

  const renderList = () => {
    let items: any[] = [];

    if (entityType === "grados") items = grados;
    else if (entityType === "areas") items = areas;
    else if (entityType === "competencias") items = competencias;
    else if (entityType === "capacidades") items = capacidades;
    else if (entityType === "temas") items = temas;
    else if (entityType === "desempenos") items = desempenos;

    if (items.length === 0) {
      return <p className="text-gray-400 text-sm">No hay registros</p>;
    }

    return (
      <div className="flex flex-wrap gap-2">
        {items.map((item) => (
          <div key={item.id} className="group relative flex items-center gap-2 bg-indigo-50 border border-indigo-200 rounded-full px-4 py-2 text-sm text-indigo-700">
            <span className="max-w-[200px] truncate">
              {item.nombre || item.descripcion}
            </span>
            <button
              onClick={() => handleEdit(item)}
              className="text-indigo-400 hover:text-indigo-600 transition shrink-0"
              title="Editar"
            >
              ✎
            </button>
            <button
              onClick={() => handleDelete(item.id)}
              className="text-red-400 hover:text-red-600 transition shrink-0"
              title="Eliminar"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    );
  };

  return (
    <DashboardLayout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Gestión Curricular</h1>
        <p className="text-sm text-gray-500 mt-1">Administra grados, áreas, competencias, capacidades, temas y desempeños</p>
      </div>

      <div className="mb-6">
        <Select
          label="Tipo de entidad"
          value={entityType}
          onChange={(e) => {
            setEntityType(e.target.value as EntityType);
            resetForm();
            setFilterAreaId("");
            setFilterCompetenciaId("");
            setFilterGradoId("");
            setFilterTemaId("");
          }}
          options={ENTITIES.map((e) => ({ value: e.value, label: e.label }))}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-bold mb-4">
            {editingId ? "Editar" : "Nuevo"} {ENTITIES.find((e) => e.value === entityType)?.label}
          </h2>
          {renderForm()}
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-bold mb-4">
            {ENTITIES.find((e) => e.value === entityType)?.label}
          </h2>
          {entityType !== "grados" && entityType !== "areas" && (
            <div className="mb-4 space-y-2">
              {(entityType === "competencias" || entityType === "temas" || entityType === "desempenos") && (
                <Select
                  label="Filtrar por área"
                  value={filterAreaId}
                  onChange={(e) => { setFilterAreaId(e.target.value); }}
                  options={[{ value: "", label: "Todas" }, ...areasOptions]}
                />
              )}
              {entityType === "temas" && (
                <Select
                  label="Filtrar por grado"
                  value={filterGradoId}
                  onChange={(e) => { setFilterGradoId(e.target.value); }}
                  options={[{ value: "", label: "Todos" }, ...gradosOptions]}
                />
              )}
              {entityType === "capacidades" && (
                <Select
                  label="Filtrar por competencia"
                  value={filterCompetenciaId}
                  onChange={(e) => { setFilterCompetenciaId(e.target.value); }}
                  options={[{ value: "", label: "Todas" }, ...competenciasOptions]}
                />
              )}
              {entityType === "desempenos" && (
                <>
                  <Select
                    label="Filtrar por grado"
                    value={filterGradoId}
                    onChange={(e) => { setFilterGradoId(e.target.value); }}
                    options={[{ value: "", label: "Todos" }, ...gradosOptions]}
                  />
                  <Select
                    label="Filtrar por tema"
                    value={filterTemaId}
                    onChange={(e) => { setFilterTemaId(e.target.value); }}
                    options={[{ value: "", label: "Todos" }, ...temasOptions]}
                  />
                </>
              )}
            </div>
          )}
          {renderList()}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default GestionCurricular;
