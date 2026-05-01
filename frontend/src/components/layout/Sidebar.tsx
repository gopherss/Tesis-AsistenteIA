import { NavLink } from "react-router-dom";
import { useAuthStore } from "../../store/auth.store";

const Sidebar = () => {
  const { user } = useAuthStore();

  const docenteMenu = [
    { name: "Panel", path: "/dashboard-docente" },
    { name: "Sesiones", path: "/sesiones" },
  ];

  const directorMenu = [
    { name: "Panel", path: "/dashboard-director" },
    { name: "Docentes", path: "/registro-docente" },
  ];

  const menu = user?.rol === "DIRECTOR" ? directorMenu : docenteMenu;

  return (
    <aside className="w-64 bg-white border-r min-h-screen">

      <div className="p-6 border-b">
        <h1 className="text-2xl font-bold text-blue-600">
          PlanIA
        </h1>
        <p className="text-sm text-gray-400">Académico</p>
      </div>

      <nav className="p-4 space-y-2">

        {menu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
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
  );
};

export default Sidebar;
