import { Link } from "react-router";

import styles from "./Sidebar.module.css";

interface SidebarButtonProps {
    text: string;
    icon: React.ReactNode;
    link: string;
    requiresServer: boolean;
}

const SidebarButton = (props: SidebarButtonProps) => {
    return (
        <Link to={props.link} className={styles.sidebarButton}>
            {props.icon}
            <span className={styles.sidebarButtonText}>{props.text}</span>
        </Link>
    )
}

export default SidebarButton;