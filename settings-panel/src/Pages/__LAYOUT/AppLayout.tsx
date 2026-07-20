import Sidebar from "./Sidebar/Sidebar";
import Footer from "./Footer/Footer";

import { useOutlet } from "react-router";

const AppLayout = () => {
    const outlet = useOutlet();

    return (
        <>
            <div className="app-content">
                <Sidebar />
                <main className="main">{outlet}</main>
            </div>
            <Footer />
        </>
    );
}

export default AppLayout;