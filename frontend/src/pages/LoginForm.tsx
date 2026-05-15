import { EyeIcon, EyeOffIcon } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Input } from '../components';
import { useAuthStore } from '../store';
import { validarEmail, validarCampoVacio } from '../utils';

const LoginForm = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [errores, setErrores] = useState<{ email?: string; password?: string }>({});
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();

    const errEmail = validarEmail(formData.email);
    const errPass = validarCampoVacio(formData.password, 'La contraseña');
    const errs: typeof errores = {};
    if (errEmail) errs.email = errEmail;
    if (errPass) errs.password = errPass;
    setErrores(errs);

    if (Object.keys(errs).length > 0) return;

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
            value={formData.email}
            onChange={(e) => {
              setFormData({ ...formData, email: e.target.value });
              setErrores((prev) => ({ ...prev, email: validarEmail(e.target.value) || undefined }));
            }}
            placeholder="correo@ejemplo.com"
            error={errores.email}
          />
          <div className="relative">
            <Input
              label="Contraseña"
              type={showPassword ? 'text' : 'password'}
              value={formData.password}
              onChange={(e) => {
                setFormData({ ...formData, password: e.target.value });
                setErrores((prev) => ({ ...prev, password: validarCampoVacio(e.target.value, 'La contraseña') || undefined }));
              }}
              placeholder="••••••••••••••••"
              error={errores.password}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-9 text-sm text-blue-600"
            >
              {showPassword ? <EyeOffIcon/> : <EyeIcon/>}
            </button>
          </div>
          <Button
            type="submit"
            label={isLoading ? 'Iniciando...' : 'Iniciar Sesión'}
            color="primary"
            disabled={isLoading}
            full
          />
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
