import { useState } from 'react';
import { useAuthStore } from '../store/auth.store';
import Input from './ui/Input';
import Button from './ui/Button';
import DashboardLayout from './layout/DashboardLayout';

const RegisterDocenteForm = () => {
  const { registerDocente, isLoading } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    nombre: '',
    apellido: '',
    rol: 'DOCENTE',
  });

  const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    const success = await registerDocente(formData);
    if (success) {
      setFormData({
        email: '',
        password: '',
        nombre: '',
        apellido: '',
        rol: 'DOCENTE',
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
            required
            value={formData.nombre}
            onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
          />
          <Input
            label="Apellido"
            required
            value={formData.apellido}
            onChange={(e) => setFormData({ ...formData, apellido: e.target.value })}
          />
          <Input
            label="Email"
            type="email"
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
          <Input
            label="Contraseña"
            type="password"
            required
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          />
          <Button
            type="submit"
            label={isLoading ? 'Registrando...' : 'Registrar Docente'}
            color="primary"
            disabled={isLoading}
          />
        </form>
      </div>
    </DashboardLayout>

  );
};

export default RegisterDocenteForm;
