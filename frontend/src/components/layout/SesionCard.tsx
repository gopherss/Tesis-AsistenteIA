import { useState } from "react";
import {
  BookOpen,
  Clock3,
  Sparkles,
  Trash2,
  RefreshCcw,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

import type { SesionResponse } from "../../types/sesion.types";
import { motion, AnimatePresence } from "framer-motion";

interface Props {
  sesion: SesionResponse & {
    contenido_ia?: string;
  };

  onDelete?: (id: number) => void;
  onRegenerar?: (id: number) => void;
}

const Badge = ({
  text,
  color,
}: {
  text: string;
  color: string;
}) => (
  <span
    className={`px-2 py-1 text-xs rounded-full font-medium ${color}`}
  >
    {text}
  </span>
);

const SesionCard = ({
  sesion,
  onDelete,
  onRegenerar,
}: Props) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden">

      {/* Header */}
      <div className="p-6 border-b bg-gradient-to-r from-indigo-50 to-blue-50">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3 className="text-xl font-bold text-slate-800">
              {sesion.titulo}
            </h3>

            <p className="text-sm text-slate-500 mt-1">
              {sesion.area} · {sesion.grado}
            </p>
          </div>

          <Badge
            text="IA"
            color="bg-indigo-100 text-indigo-700"
          />
        </div>

        <p className="mt-4 text-slate-600 text-sm leading-relaxed">
          {sesion.proposito}
        </p>
      </div>

      {/* Body */}
      <div className="p-6 space-y-4">

        {/* Meta */}
        <div className="grid grid-cols-2 gap-4 text-sm">

          <div className="flex items-center gap-2 text-slate-600">
            <BookOpen size={16} />
            <span>{sesion.tema}</span>
          </div>

          <div className="flex items-center gap-2 text-slate-600">
            <Clock3 size={16} />
            <span>{sesion.tiempo_sesion} min</span>
          </div>

        </div>

        {/* Chips */}
        <div className="flex flex-wrap gap-2">
          {sesion.competencias?.slice(0, 3).map((item, i) => (
            <Badge
              key={i}
              text={item}
              color="bg-emerald-100 text-emerald-700"
            />
          ))}
        </div>

        {/* IA Preview */}
        {sesion.contenido_ia && (
          <div className="bg-slate-50 border rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles size={16} className="text-indigo-600" />
              <span className="font-semibold text-sm text-slate-700">
                Contenido generado por IA
              </span>
            </div>

            <p className="text-sm text-slate-600 line-clamp-3 whitespace-pre-line">
              {sesion.contenido_ia}
            </p>
          </div>
        )}

        {/* Expand */}
        <button
          onClick={() => setOpen(!open)}
          className="text-sm text-indigo-600 font-medium flex items-center gap-1 hover:text-indigo-700"
        >
          {open ? (
            <>
              Ver menos <ChevronUp size={16} />
            </>
          ) : (
            <>
              Ver más <ChevronDown size={16} />
            </>
          )}
        </button>

        <AnimatePresence>

          {open && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.28 }}
              className="overflow-hidden"

            >
              <div className="space-y-4 pt-2">

                {/* Capacidades */}
                <div>
                  <h4 className="font-semibold text-sm mb-2 text-slate-700">
                    Capacidades
                  </h4>

                  <div className="flex flex-wrap gap-2">
                    {sesion.capacidades?.map((c, i) => (
                      <Badge
                        key={i}
                        text={c}
                        color="bg-blue-100 text-blue-700"
                      />
                    ))}
                  </div>
                </div>

                {/* Desempeño */}
                <div>
                  <h4 className="font-semibold text-sm mb-2 text-slate-700">
                    Desempeño
                  </h4>

                  <div className="flex flex-wrap gap-2">
                    {sesion.desempeno?.map((d, i) => (
                      <Badge
                        key={i}
                        text={d}
                        color="bg-yellow-100 text-yellow-700"
                      />
                    ))}
                  </div>
                </div>

                {/* IA Full */}
                {sesion.contenido_ia && (
                  <div>
                    <h4 className="font-semibold text-sm mb-2 text-slate-700">
                      Sesión completa IA
                    </h4>

                    <div className="bg-slate-50 border rounded-xl p-4 text-sm whitespace-pre-line text-slate-700 max-h-96 overflow-y-auto">
                      {sesion.contenido_ia}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </div>

      {/* Footer */}
      <div className="px-6 py-4 border-t bg-slate-50 flex flex-wrap gap-2">
        <button
          className="px-4 py-2 rounded-xl border text-sm font-medium hover:bg-white flex items-center gap-2"
          onClick={() => onRegenerar?.(sesion.id)}
        >
          <RefreshCcw size={16} />
          Regenerar IA
        </button>

        <button
          className="px-4 py-2 rounded-xl border text-sm font-medium text-red-600 hover:bg-red-50 flex items-center gap-2"
          onClick={() => onDelete?.(sesion.id)}
        >
          <Trash2 size={16} />
          Eliminar
        </button>

      </div>
    </div>
  );
};

export default SesionCard;
