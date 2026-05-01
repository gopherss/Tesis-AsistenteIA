import { DashboardLayout } from '../components';
import { useAuthStore } from '../store/auth.store';

const DirectorDashboard = () => {
  const { user } = useAuthStore();

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm">
          <h1>Bienvenido {user?.nombre}</h1>
        </nav>
      </div>
    </DashboardLayout>
  );
};

export default DirectorDashboard;
