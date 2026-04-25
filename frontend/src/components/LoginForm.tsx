import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth.store';
import Input from './ui/Input';
import Button from './ui/Button';

const LoginForm = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    const success = await login(formData);
    if (success) {
      const user = useAuthStore.getState().user;
      if (user?.rol === 'DIRECTOR') {
        navigate('/dashboard-director');
      }
      
      if (user?.rol === 'DOCENTE') {
        navigate('/dashboard-docente');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
        <div>
          <h2 className="text-3xl font-bold text-center text-gray-900">
            Iniciar Sesión
          </h2>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Email"
            type="email"
            required
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            placeholder="correo@ejemplo.com"
          />
          <Input
            label="Contraseña"
            type="password"
            required
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            placeholder="••••••••"
          />
          <Button
            type="submit"
            label={isLoading ? 'Iniciando...' : 'Iniciar Sesión'}
            color="primary"
            disabled={isLoading}
          />
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
