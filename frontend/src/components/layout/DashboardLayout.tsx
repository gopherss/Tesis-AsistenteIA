import Sidebar from "./Sidebar";
import Topbar from "./Topbar";


const DashboardLayout = ({
    children,
}: {
    children: React.ReactNode;
}) => {
    return (
        <div className="flex bg-gray-50 min-h-2">

            <Sidebar />

            <div className="flex-1">

                <Topbar />

                <main className="p-8">{children}</main>

            </div>
        </div>
    );
};

export default DashboardLayout;
