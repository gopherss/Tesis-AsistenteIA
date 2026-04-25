import { useEffect } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Toaster } from 'sonner';
import { Dashboard, DocenteDashboard, LoginForm, RegisterDocenteForm } from './components';
import { useAuthStore } from './store/auth.store';

const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode; allowedRoles?: string[] }) => {
  const { user, token } = useAuthStore();

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.rol)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
};

const App = () => {
  const { loadUser } = useAuthStore();

  useEffect(() => {
    loadUser();
  }, []);

  return (
    <BrowserRouter>
      <Toaster position="top-right" richColors />
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route
          path="/dashboard-director"
          element={
            <ProtectedRoute allowedRoles={['DIRECTOR']}>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/registro-docente"
          element={
            <ProtectedRoute allowedRoles={['DIRECTOR']}>
              <RegisterDocenteForm />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path='*' element={<Navigate to="/login" replace />} />
        <Route
          path='/dashboard-docente'
          element={
            <ProtectedRoute allowedRoles={['DOCENTE']}>
              <DocenteDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
