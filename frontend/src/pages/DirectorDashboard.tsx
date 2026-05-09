import { DashboardLayout } from '../components';
import { useAuthStore } from '../store';

const DirectorDashboard = () => {
  const { user } = useAuthStore();

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm">
          <h1 className='text-cyan-500 text-center'>Bienvenido {user?.nombre}</h1>
        </nav>
      </div>
    </DashboardLayout>
  );
};

export default DirectorDashboard;
