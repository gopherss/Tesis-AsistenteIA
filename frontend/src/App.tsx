import { useEffect } from 'react';
import { Toaster } from 'sonner';
import { useAuthStore } from './store/auth.store';
import ProtectedRoute from './routes/ProtectedRoute';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import DirectorDashboard, { DocenteDashboard, LoginForm, RegisterDocenteForm } from './pages';
import Sesiones from './pages/Sesiones';
import Estudiantes from './pages/Estudiantes';

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
        <Route
          path='/estudiantes'
          element={
            <ProtectedRoute allowedRoles={['DOCENTE']}>
              <Estudiantes/>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
