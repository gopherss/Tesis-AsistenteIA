import { Input } from "../index";
import UserMenu from "../ui/UserMenu";

const Topbar = () => {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-4 md:px-6 gap-4">

      <div className="hidden sm:block w-64 md:w-96">
        <Input placeholder="Buscar sesiones..." />
      </div>

      <button className="sm:hidden p-2 text-gray-600 hover:text-blue-600">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>

      <div className="flex items-center gap-4">
        <UserMenu />
      </div>
    </header>
  );
};

export default Topbar;
