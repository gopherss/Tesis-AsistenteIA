import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useAuthStore } from "../../store";
import { Menu, X } from "lucide-react";

const Sidebar = () => {
  const { user } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);

  const docenteMenu = [
    { name: "Panel", path: "/dashboard-docente" },
    { name: "Sesiones", path: "/sesiones" },
  ];

  const directorMenu = [
    { name: "Panel", path: "/dashboard-director" },
    { name: "Docentes", path: "/registro-docente" },
    { name: "Currículo", path: "/gestion-curricular" },
  ];

  const menu = user?.rol === "DIRECTOR" ? directorMenu : docenteMenu;

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-blue-600 text-white rounded-lg shadow-lg"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      <aside
        className={`
          fixed lg:relative z-50
          w-64 bg-white border-r min-h-screen
          transition-transform duration-300 ease-in-out
          ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
        `}
      >
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-600">PlanIA</h1>
          <p className="text-sm text-gray-400">Académico</p>
        </div>

        <nav className="p-4 space-y-2">
          {menu.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setIsOpen(false)}
              className={({ isActive }) =>
                `block px-4 py-3 rounded-xl transition ${
                  isActive
                    ? "bg-blue-100 text-blue-600 font-semibold"
                    : "hover:bg-gray-100 text-gray-600"
                }`
              }
            >
              {item.name}
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;