import { useState } from 'react';
import { useAuthStore } from '../store/auth.store';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import DashboardLayout from '../components/layout/DashboardLayout';
import type { RegisterDocenteData } from '../types/auth.types';
import { toast } from 'sonner';

const RegisterDocenteForm = () => {
  const { registerDocente, isLoading } = useAuthStore();
  const [formData, setFormData] = useState<RegisterDocenteData>({
    email: '',
    password: '',
    nombre: '',
    apellido: '',
    rol: 'DOCENTE',
  });

  const handleSubmit = async (
    e: React.SyntheticEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    const nombre = formData.nombre.trim();
    const apellido = formData.apellido.trim();
    const email = formData.email.trim().toLowerCase();
    const password = formData.password.trim();

    if (!nombre) {
      toast.warning("Ingrese el nombre");
      return;
    }

    if (!apellido) {
      toast.warning("Ingrese el apellido");
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      toast.warning("Ingrese un correo válido");
      return;
    }

    if (!password) {
      toast.warning("Ingrese una contraseña");
      return;
    }

    if (password.length < 6) {
      toast.warning("La contraseña debe tener mínimo 6 caracteres");
      return;
    }

    const success = await registerDocente({
      ...formData,
      nombre,
      apellido,
      email,
      password,
    });

    if (success) {
      setFormData({
        email: "",
        password: "",
        nombre: "",
        apellido: "",
        rol: "DOCENTE",
      });
    }
  };

  return (
    <DashboardLayout>

      <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-6">Registrar Nuevo Docente</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Nombre"
            value={formData.nombre}
            onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
          />
          <Input
            label="Apellido"
            value={formData.apellido}
            onChange={(e) => setFormData({ ...formData, apellido: e.target.value })}
          />
          <Input
            label="Email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
          <Input
            label="Contraseña"
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          />
          <Button
            type="submit"
            label={isLoading ? 'Registrando...' : 'Registrar Docente'}
            color="primary"
            disabled={isLoading}
            full
          />
        </form>
      </div>
    </DashboardLayout>

  );
};

export default RegisterDocenteForm;
