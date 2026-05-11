import { useEffect, useMemo, useState } from "react";
import {
  BookOpen, Clock3, Sparkles, Trash2, RefreshCcw, ChevronDown, ChevronUp, Download, Pencil,
} from "lucide-react";
import type { SesionResponse, SesionUpdateData } from "../../types/sesion.types";
import type { Competencia, Capacidad, Desempeno } from "../../types/curriculum.types";
import { motion, AnimatePresence } from "framer-motion";
import { descargarPdfSesion } from "../../services/sesion.service";
import { curriculumService } from "../../services/curriculum.service";
import { useCurriculumStore, useSesionStore } from "../../store";
import { Select, Input, Button } from "..";

interface Props {
  sesion: SesionResponse;
  onDelete?: (id: number) => void;
  onRegenerar?: (id: number) => void;
}

const Badge = ({ text, color }: { text: string; color: string }) => (
  <span className={`px-2 py-1 text-xs rounded-full font-medium ${color}`}>{text}</span>
);

const SesionCard = ({ sesion, onDelete, onRegenerar }: Props) => {
  const { actualizarSesion } = useSesionStore();
  const { areas, grados, temas, cargarAreas, cargarGrados, cargarTemas } = useCurriculumStore();

  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  const [competencias, setCompetencias] = useState<Competencia[]>([]);
  const [capacidades, setCapacidades] = useState<Capacidad[]>([]);
  const [desempenos, setDesempenos] = useState<Desempeno[]>([]);

  const [form, setForm] = useState<SesionUpdateData>({
    titulo: sesion.titulo,
    proposito: sesion.proposito,
    grado: sesion.grado,
    area: sesion.area,
    tema: sesion.tema,
    competencias: sesion.competencias || [],
    capacidades: sesion.capacidades || [],
    desempeno: sesion.desempeno || [],
    numero_ejercicios: sesion.numero_ejercicios,
    tiempo_sesion: sesion.tiempo_sesion,
  });
  const selectedCompetencias = form.competencias;
  const selectedCapacidades = form.capacidades;
  const selectedDesempenos = form.desempeno;

  useEffect(() => {
    cargarAreas();
    cargarGrados();
  }, []);

  const areaObj = useMemo(() => areas.find((a: any) => a.nombre === form.area), [areas, form.area]);
  const gradoObj = useMemo(() => grados.find((g: any) => g.nombre === form.grado), [grados, form.grado]);
  const temaObj = useMemo(() => temas.find((t: any) => t.nombre === form.tema), [temas, form.tema]);

  useEffect(() => {
    if (areaObj?.id && gradoObj?.id) {
      cargarTemas(areaObj.id, gradoObj.id);
    }
  }, [areaObj?.id, gradoObj?.id]);

  useEffect(() => {
    if (areaObj?.id) {
      curriculumService.getCompetencias(areaObj.id).then(setCompetencias).catch(() => {});
    }
  }, [areaObj?.id]);

  useEffect(() => {
    if (temaObj?.id) {
      curriculumService.getDesempenos(temaObj.id).then(setDesempenos).catch(() => {});
    } else {
      setDesempenos([]);
    }
  }, [temaObj?.id]);

  const handleField = (field: keyof SesionUpdateData, value: any) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setDirty(true);
  };

  const toggleTag = (list: string[], setter: (list: string[]) => void, value: string) => {
    const next = list.includes(value) ? list.filter((x) => x !== value) : [...list, value];
    setter(next);
    setDirty(true);
  };

  const selectCompetencia = (nombre: string) => {
    toggleTag(selectedCompetencias, (v) => handleField("competencias", v), nombre);
    if (!selectedCompetencias.includes(nombre)) {
      const c = competencias.find((x) => x.nombre === nombre);
      if (c) curriculumService.getCapacidades(c.id).then(setCapacidades).catch(() => {});
    }
  };

  const handleGuardar = async () => {
    const ok = await actualizarSesion(sesion.id, form);
    if (ok) {
      setEditing(false);
      setDirty(false);
    }
  };

  const handleDescargarPDF = async () => {
    setIsDownloading(true);
    try {
      await descargarPdfSesion(sesion.id);
    } catch {
      console.error("Error al descargar PDF");
    } finally {
      setIsDownloading(false);
    }
  };

  const areaOptions = areas.map((a: any) => ({ value: a.nombre, label: a.nombre }));
  const gradoOptions = grados.map((g: any) => ({ value: g.nombre, label: g.nombre }));
  const temaOptions = temas.map((t: any) => ({ value: t.nombre, label: t.nombre }));

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden">
      {editing ? (
        <div className="p-6 space-y-4">
          <h3 className="text-lg font-bold text-slate-800">Editar sesión</h3>
          <div className="grid grid-cols-2 gap-3">
            <Input label="Título" value={form.titulo} onChange={(e) => handleField("titulo", e.target.value)} />
            <Input label="Propósito" value={form.proposito} onChange={(e) => handleField("proposito", e.target.value)} />
            <Select label="Grado" value={form.grado} onChange={(e) => handleField("grado", e.target.value)} options={gradoOptions} placeholder="Grado" />
            <Select label="Área" value={form.area} onChange={(e) => { handleField("area", e.target.value); handleField("tema", ""); }} options={areaOptions} placeholder="Área" />
          </div>
          <div>
            <Select label="Tema" value={form.tema} onChange={(e) => handleField("tema", e.target.value)} options={temaOptions} placeholder="Tema" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Competencias</label>
            <div className="flex flex-wrap gap-2">
              {competencias.map((c) => (
                <button key={c.id} type="button" onClick={() => selectCompetencia(c.nombre)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${selectedCompetencias.includes(c.nombre) ? "bg-emerald-600 text-white" : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`}
                >{c.nombre}</button>
              ))}
            </div>
          </div>

          {selectedCompetencias.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Capacidades</label>
              <div className="flex flex-wrap gap-2">
                {capacidades.map((c) => (
                  <button key={c.id} type="button" onClick={() => toggleTag(selectedCapacidades, (v) => handleField("capacidades", v), c.nombre)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${selectedCapacidades.includes(c.nombre) ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`}
                  >{c.nombre}</button>
                ))}
              </div>
            </div>
          )}

          {desempenos.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Desempeños</label>
              <div className="flex flex-wrap gap-2">
                {desempenos.map((d) => (
                  <button key={d.id} type="button" onClick={() => toggleTag(selectedDesempenos, (v) => handleField("desempeno", v), d.descripcion)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${selectedDesempenos.includes(d.descripcion) ? "bg-yellow-600 text-white" : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`}
                  >{d.descripcion}</button>
                ))}
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            <Input label="Ejercicios" type="number" min={1} value={form.numero_ejercicios} onChange={(e) => handleField("numero_ejercicios", Number(e.target.value))} />
            <Input label="Tiempo (min)" type="number" min={10} value={form.tiempo_sesion} onChange={(e) => handleField("tiempo_sesion", Number(e.target.value))} />
          </div>

          <div className="flex gap-2">
            <Button label="Guardar" color="primary" onClick={handleGuardar} />
            <Button label="Cancelar" color="secondary" onClick={() => { setEditing(false); setDirty(false); }} />
          </div>
        </div>
      ) : (
        <>
          <div className="p-6 border-b bg-gradient-to-r from-indigo-50 to-blue-50">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-xl font-bold text-slate-800">{sesion.titulo}</h3>
                <p className="text-sm text-slate-500 mt-1">{sesion.area} · {sesion.grado}</p>
              </div>
              <Badge text="IA" color="bg-indigo-100 text-indigo-700" />
            </div>
            <p className="mt-4 text-slate-600 text-sm leading-relaxed">{sesion.proposito}</p>
          </div>

          <div className="p-6 space-y-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="flex items-center gap-2 text-slate-600"><BookOpen size={16} /><span>{sesion.tema}</span></div>
              <div className="flex items-center gap-2 text-slate-600"><Clock3 size={16} /><span>{sesion.tiempo_sesion} min</span></div>
            </div>

            <div className="flex flex-wrap gap-2">
              {sesion.competencias?.slice(0, 3).map((item, i) => (
                <Badge key={i} text={item} color="bg-emerald-100 text-emerald-700" />
              ))}
            </div>

            {sesion.contenido_ia && (
              <div className="bg-slate-50 border rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles size={16} className="text-indigo-600" />
                  <span className="font-semibold text-sm text-slate-700">Contenido generado por IA</span>
                </div>
                <p className="text-sm text-slate-600 line-clamp-3 whitespace-pre-line">{sesion.contenido_ia}</p>
              </div>
            )}

            <button onClick={() => setOpen(!open)} className="text-sm text-indigo-600 font-medium flex items-center gap-1 hover:text-indigo-700">
              {open ? <>Ver menos <ChevronUp size={16} /></> : <>Ver más <ChevronDown size={16} /></>}
            </button>

            <AnimatePresence>
              {open && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} transition={{ duration: 0.28 }} className="overflow-hidden">
                  <div className="space-y-4 pt-2">
                    <div>
                      <h4 className="font-semibold text-sm mb-2 text-slate-700">Capacidades</h4>
                      <div className="flex flex-wrap gap-2">
                        {sesion.capacidades?.map((c, i) => (<Badge key={i} text={c} color="bg-blue-100 text-blue-700" />))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold text-sm mb-2 text-slate-700">Desempeño</h4>
                      <div className="flex flex-wrap gap-2">
                        {sesion.desempeno?.map((d, i) => (<Badge key={i} text={d} color="bg-yellow-100 text-yellow-700" />))}
                      </div>
                    </div>
                    {sesion.contenido_ia && (
                      <div>
                        <h4 className="font-semibold text-sm mb-2 text-slate-700">Sesión completa IA</h4>
                        <div className="bg-slate-50 border rounded-xl p-4 text-sm whitespace-pre-line text-slate-700 max-h-96 overflow-y-auto">{sesion.contenido_ia}</div>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </>
      )}

      <div className="px-6 py-4 border-t bg-slate-50 flex flex-wrap gap-2">
        <button className="px-4 py-2 rounded-xl border text-sm font-medium hover:bg-blue-50 flex items-center gap-2 text-blue-600" onClick={handleDescargarPDF} disabled={isDownloading}>
          <Download size={16} />{isDownloading ? "Descargando..." : "Descargar PDF"}
        </button>

        <button
          className={`px-4 py-2 rounded-xl border text-sm font-medium flex items-center gap-2 ${dirty ? "bg-amber-500 text-white hover:bg-amber-600" : "text-gray-400 cursor-not-allowed"}`}
          onClick={() => onRegenerar?.(sesion.id)}
          disabled={!dirty}
        >
          <RefreshCcw size={16} />Regenerar IA
        </button>

        <button className="px-4 py-2 rounded-xl border text-sm font-medium hover:bg-green-50 flex items-center gap-2 text-green-600" onClick={() => setEditing(true)}>
          <Pencil size={16} />Editar
        </button>

        <button className="px-4 py-2 rounded-xl border text-sm font-medium text-red-600 hover:bg-red-50 flex items-center gap-2" onClick={() => onDelete?.(sesion.id)}>
          <Trash2 size={16} />Eliminar
        </button>
      </div>
    </div>
  );
};

export default SesionCard;
