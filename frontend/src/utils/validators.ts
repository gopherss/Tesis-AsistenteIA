const REGEX_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validarEmail(email: string): string | null {
  if (!email.trim()) return "El email es obligatorio";
  if (!REGEX_EMAIL.test(email)) return "Formato de email inválido";
  return null;
}

export function validarPassword(password: string): string | null {
  if (!password) return "La contraseña es obligatoria";
  if (password.length < 6) return "Debe tener al menos 6 caracteres";
  if (!/[a-zA-Z]/.test(password)) return "Debe contener al menos una letra";
  if (!/[0-9]/.test(password)) return "Debe contener al menos un número";
  return null;
}

export function validarCampoVacio(valor: string, nombre: string): string | null {
  if (!valor.trim()) return `${nombre} es obligatorio`;
  return null;
}

export function validarNombre(valor: string, nombre: string): string | null {
  const err = validarCampoVacio(valor, nombre);
  if (err) return err;
  if (valor.trim().length < 2) return `${nombre} debe tener al menos 2 caracteres`;
  if (!/^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$/.test(valor.trim())) return `${nombre} solo debe contener letras`;
  return null;
}

export interface ErroresRegistro {
  nombre?: string;
  apellido?: string;
  email?: string;
  password?: string;
}

export function validarFormularioRegistro(data: {
  nombre: string;
  apellido: string;
  email: string;
  password: string;
}): ErroresRegistro {
  const errores: ErroresRegistro = {};
  const nombreErr = validarNombre(data.nombre, "Nombre");
  if (nombreErr) errores.nombre = nombreErr;
  const apellidoErr = validarNombre(data.apellido, "Apellido");
  if (apellidoErr) errores.apellido = apellidoErr;
  const emailErr = validarEmail(data.email);
  if (emailErr) errores.email = emailErr;
  const passErr = validarPassword(data.password);
  if (passErr) errores.password = passErr;
  return errores;
}

export interface ErroresEdicion {
  nombre?: string;
  apellido?: string;
  email?: string;
}

export function validarFormularioEdicion(data: {
  nombre: string;
  apellido: string;
  email: string;
}): ErroresEdicion {
  const errores: ErroresEdicion = {};
  const nombreErr = validarNombre(data.nombre, "Nombre");
  if (nombreErr) errores.nombre = nombreErr;
  const apellidoErr = validarNombre(data.apellido, "Apellido");
  if (apellidoErr) errores.apellido = apellidoErr;
  const emailErr = validarEmail(data.email);
  if (emailErr) errores.email = emailErr;
  return errores;
}
