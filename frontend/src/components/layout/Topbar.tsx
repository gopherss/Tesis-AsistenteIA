import { Input } from "../index";
import UserMenu from "../ui/UserMenu";

const Topbar = () => {

  return (
    <>
      <header className="h-16 bg-white border-b flex items-center justify-between px-6 gap-4">
        <div className="w-96">
          <Input placeholder="Buscar sesiones..." />
        </div>

        <div className="flex items-center gap-4">
         
          <UserMenu/>
        </div>
      </header>    
    </>
  );
};

export default Topbar;