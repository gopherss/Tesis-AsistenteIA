import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/auth.store";
import DashboardLayout from "./layout/DashboardLayout";
import Button from "./ui/Button";

const DocenteDashboard = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();


  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };
  return (
    <DashboardLayout>

    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold">Dashboard Docente</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span>{user?.nombre} {user?.apellido}</span>
              <Button label="Cerrar Sesión" color="danger" onClick={handleLogout} />
            </div>
          </div>
        </div>
      </nav>

    </div>
    </DashboardLayout>

  );
};

export default DocenteDashboard;
