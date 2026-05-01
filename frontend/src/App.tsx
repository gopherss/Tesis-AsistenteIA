import { useEffect } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Toaster } from 'sonner';
import DirectorDashboard, { DocenteDashboard, LoginForm, RegisterDocenteForm } from './pages';
import Sesiones from './pages/Sesiones';
import ProtectedRoute from './routes/ProtectedRoute';
import { useAuthStore } from './store/auth.store';

const App = () => {
  const { loadUser } = useAuthStore();

  useEffect(() => {
    loadUser();
  }, []);

  return (
    <BrowserRouter>
      <Toaster position="bottom-right" richColors />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path='*' element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginForm />} />
        <Route
          path="/dashboard-director"
          element={
            <ProtectedRoute allowedRoles={['DIRECTOR']}>
              <DirectorDashboard />
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
        <Route
          path='/dashboard-docente'
          element={
            <ProtectedRoute allowedRoles={['DOCENTE']}>
              <DocenteDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path='/sesiones'
          element={
            <ProtectedRoute allowedRoles={['DOCENTE']}>
              <Sesiones/>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
