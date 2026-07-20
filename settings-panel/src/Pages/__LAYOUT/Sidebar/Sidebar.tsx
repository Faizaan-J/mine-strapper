
import { NavLink } from "react-router";

import ServerSelectionState from "./ServerSelectionState";

import { BoxPixelIcon, CogPixelIcon, HomePixelIcon, InfoPixelIcon, StateStylesPixelIcon } from "@components/Icons/PixelIcon";
import SidebarButton from "./SidebarButton";

type NavLinkItem = {
    label: string;
    path: string;
    icon: React.ReactNode;
    requiresServer?: boolean;
};

const Sidebar = () => {
    // const { selectedServer, hasServer } = useServerEditor();
    const selectedServer = {
        displayName: "Example Server",
        rootPath: "/path/to/server",
    };
    const hasServer = false;

    const configLinks: NavLinkItem[] = [{ label: "Server", path: "/server", icon: <CogPixelIcon />, requiresServer: true }];
    const featureLinks: NavLinkItem[] = [
        { label: "State Styles", path: "/state-styles", icon: <StateStylesPixelIcon />, requiresServer: true },
        { label: "Resource Pack", path: "/resource-pack", icon: <BoxPixelIcon />, requiresServer: true },
    ];

    return (
        <aside className="sidebar">
                <ServerSelectionState />
                <nav className="sidebar-nav">
                    <SidebarLink path="/" icon={<HomePixelIcon />} label="Home" />

                    <SectionLabel label="Configuration" />
                    {configLinks.map((link) => (
                        <SidebarButton key={link.path} link={link.path} text={link.label} icon={link.icon} requiresServer={link.requiresServer || false} />
                    ))}

                    <SectionLabel label="Built-in features" />
                    {featureLinks.map((link) => (
                        <SidebarButton key={link.path} link={link.path} text={link.label} icon={link.icon} requiresServer={link.requiresServer || false} />
                    ))}

                    <div className="sidebar-spacer" />

                    <SectionLabel label="Other" />
                    <SidebarButton link="/about" icon={<InfoPixelIcon />} text="About" requiresServer={false} />
                </nav>
        </aside>
    );
};

const SectionLabel = ({ label }: { label: string }) => <div className="sidebar-section-label">{label}</div>;

const SidebarLink = ({ label, path, icon, disabled }: NavLinkItem & { disabled?: boolean }) => {
    if (disabled) {
        return (
            <span className="sidebar-link sidebar-link-disabled" aria-disabled="true">
                {icon}
                <span>{label}</span>
            </span>
        );
    }
    
    let isActive = "isActive";

    return (
        <NavLink to={path} className={`sidebar-link ${isActive ? "sidebar-link-active" : ""}`.trim()}>
            {icon}
            <span>{label}</span>
        </NavLink>
    );
};

export default Sidebar;
