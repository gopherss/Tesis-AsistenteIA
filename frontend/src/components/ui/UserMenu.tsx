import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../index";
import { useAuthStore } from "../../store";

const UserMenu = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const [openMenu, setOpenMenu] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target as Node)
      ) {
        setOpenMenu(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };
  }, []);

  return (
    <div className="relative" ref={menuRef}>

      {/* AVATAR */}
      <button
        onClick={() => setOpenMenu(!openMenu)}
        className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold cursor-pointer hover:bg-blue-700 transition-all"
      >
        {user?.nombre?.charAt(0)}
      </button>

      {openMenu && (
        <div className="absolute right-0 mt-2 w-56 bg-white border rounded-xl shadow-xl p-3 z-50">

          <div className="mb-3 border-b pb-2">
            <p className="font-semibold text-gray-800 text-center">
               {user?.nombre} {user?.apellido}
            </p>

          </div>

          <Button
            label="Cerrar Sesión"
            color="danger"
            full
            onClick={handleLogout}
          />

        </div>
      )}
    </div>
  );
};

export default UserMenu;