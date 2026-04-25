import { useState } from "react";
import { useAuthStore } from "../../store/auth.store";
import { useDocenteStore } from "../../store/docente.store";
import { Button, Input } from "../index";
import UserMenu from "../ui/UserMenu";

const Topbar = () => {
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

  const abrirChat = async () => {
    setOpenChat(true);

    if (chat.length === 0) {
      await iniciarChat();
    }
  };

  const seleccionar = (valor: string) => {
    if (step === 1) {
      setContexto((prev) => ({
        ...prev,
        nivel: valor,
      }));
      setStep(2);
      return;
    }

    if (step === 2) {
      setContexto((prev) => ({
        ...prev,
        grado: valor,
      }));
      setStep(3);
      return;
    }
  };

  const enviar = async () => {
    if (!mensaje.trim()) return;

    if (step === 3) {
      setContexto((prev) => ({
        ...prev,
        curso: mensaje,
      }));

      setMensaje("");
      setStep(4);
      return;
    }

    // TEMA
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

    await enviarMensaje(mensaje);
    setMensaje("");
  };

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
      <header className="h-16 bg-white border-b flex items-center justify-between px-6 gap-4">
        <div className="w-96">
          <Input placeholder="Buscar sesiones..." />
        </div>

        <div className="flex items-center gap-4">
          {
            user?.rol === "DOCENTE" && (
                        <Button
            label="Generar con IA"
            color="primary"
            onClick={abrirChat}
          /> )

          }

          <UserMenu/>
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
                x
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

              {/* PASOS */}
              {step <= 4 && (
                <div className="space-y-3">
                  <p className="text-sm text-gray-500">
                    {textoPaso()}
                  </p>

                  {step <= 2 && (
                    <div className="flex flex-wrap gap-2">
                      {renderTags().map((tag) => (
                        <Button
                          key={tag}
                          label={tag}
                          color="secondary"
                          onClick={() => seleccionar(tag)}
                        />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* INPUT CHAT */}
            <div className="p-4 border-t flex gap-2 items-end">

              <div className="flex-1">
                <Input
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
                />
              </div>

              <Button
                label="Enviar"
                color="primary"
                onClick={enviar}
                disabled={!mensaje.trim() && step >= 3}
              />
            </div>

          </div>
        </div>
      )}
    </>
  );
};

export default Topbar;