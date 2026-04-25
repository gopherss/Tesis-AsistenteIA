import { useState } from "react";
import { useAuthStore } from "../../store/auth.store";
import { useDocenteStore } from "../../store/docente.store";

export const Topbar = () => {
  const { user } = useAuthStore();
  const { chat, iniciarChat, enviarMensaje } = useDocenteStore();

  const [openChat, setOpenChat] = useState(false);
  const [mensaje, setMensaje] = useState("");

  const [step, setStep] = useState(1);

  const [contexto, setContexto] = useState({
    nivel: "",
    grado: "",
    curso: "",
    tema: "",
  });

  // ==========================================
  // ABRIR CHAT
  // ==========================================
  const abrirChat = async () => {
    setOpenChat(true);

    if (chat.length === 0) {
      await iniciarChat();
    }
  };

  // ==========================================
  // SELECCION TAGS
  // ==========================================
  const seleccionar = (valor: string) => {
    // NIVEL
    if (step === 1) {
      setContexto({
        ...contexto,
        nivel: valor,
      });

      setStep(2);
      return;
    }

    // GRADO
    if (step === 2) {
      setContexto({
        ...contexto,
        grado: valor,
      });

      setStep(3);
      return;
    }
  };

  // ==========================================
  // ENVIAR MENSAJE
  // ==========================================
  const enviar = async () => {
    if (!mensaje.trim()) return;

    // PASO 3 = CURSO
    if (step === 3) {
      setContexto({
        ...contexto,
        curso: mensaje,
      });

      setMensaje("");
      setStep(4);
      return;
    }

    // PASO 4 = TEMA
    if (step === 4) {
      const nuevo = {
        ...contexto,
        tema: mensaje,
      };

      setContexto(nuevo);
      setMensaje("");
      setStep(5);

      await enviarMensaje(`
Soy docente de:

Nivel: ${nuevo.nivel}
Grado: ${nuevo.grado}
Curso: ${nuevo.curso}
Tema: ${nuevo.tema}

Ayúdame con este tema.
      `);

      return;
    }

    // CHAT NORMAL
    await enviarMensaje(mensaje);
    setMensaje("");
  };

  // ==========================================
  // TAGS DINAMICOS
  // ==========================================
  const renderTags = () => {
    if (step === 1) {
      return ["Inicial", "Primaria", "Secundaria"];
    }

    if (step === 2) {
      if (contexto.nivel === "Primaria") {
        return ["1ro", "2do", "3ro", "4to", "5to", "6to"];
      }

      if (contexto.nivel === "Secundaria") {
        return ["1ro", "2do", "3ro", "4to", "5to"];
      }

      if (contexto.nivel === "Inicial") {
        return ["3 años", "4 años", "5 años"];
      }
    }

    return [];
  };

  // ==========================================
  // TEXTO GUIA
  // ==========================================
  const textoPaso = () => {
    if (step === 1) return "Selecciona tu nivel";
    if (step === 2) return "Selecciona tu grado";
    if (step === 3) return "Escribe el curso que dictas";
    if (step === 4) return "Escribe el tema de hoy";
    return "";
  };

  return (
    <>
      {/* TOPBAR */}
      <header className="h-16 bg-white border-b flex items-center justify-between px-6">
        <input
          placeholder="Buscar sesiones..."
          className="border rounded-xl px-4 py-2 w-96"
        />

        <div className="flex items-center gap-4">
          <button
            onClick={abrirChat}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl"
          >
            Generar con IA
          </button>

          <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
            {user?.nombre?.charAt(0)}
          </div>
        </div>
      </header>

      {/* MODAL CHAT */}
      {openChat && (
        <div className="fixed inset-0 bg-black/40 z-50 flex justify-end">

          <div className="w-[430px] h-full bg-white shadow-2xl flex flex-col">

            {/* HEADER */}
            <div className="p-4 border-b flex justify-between items-center">
              <div>
                <h2 className="font-bold text-lg text-gray-800">
                  Asistente IA
                </h2>

                <p className="text-sm text-gray-500">
                  Docente {user?.nombre}
                </p>
              </div>

              <button
                onClick={() => setOpenChat(false)}
                className="text-gray-500 text-xl"
              >
                ×
              </button>
            </div>

            {/* MENSAJES */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">

              {chat.map((msg, index) => (
                <div
                  key={index}
                  className={`max-w-[85%] p-3 rounded-2xl text-sm whitespace-pre-line ${
                    msg.tipo === "user"
                      ? "ml-auto bg-blue-600 text-white"
                      : "bg-white border text-gray-800"
                  }`}
                >
                  {msg.texto}
                </div>
              ))}

              {/* PASOS GUIADOS */}
              {step <= 4 && (
                <div className="space-y-3">

                  <p className="text-sm text-gray-500">
                    {textoPaso()}
                  </p>

                  {/* TAGS */}
                  {step <= 2 && (
                    <div className="flex flex-wrap gap-2">
                      {renderTags().map((tag) => (
                        <button
                          key={tag}
                          onClick={() => seleccionar(tag)}
                          className="px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-sm hover:bg-blue-200"
                        >
                          {tag}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* INPUT */}
            <div className="p-4 border-t flex gap-2">
              <input
                value={mensaje}
                onChange={(e) => setMensaje(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") enviar();
                }}
                placeholder={
                  step === 3
                    ? "Ej: Matemática"
                    : step === 4
                    ? "Ej: Fracciones equivalentes"
                    : "Escribe tu mensaje..."
                }
                className="flex-1 border rounded-xl px-4 py-2"
              />

              <button
                onClick={enviar}
                disabled={!mensaje.trim() && step >= 3}
                className="bg-blue-600 text-white px-4 rounded-xl disabled:opacity-50"
              >
                Enviar
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
};
