import styles from "./Sidebar.module.css";

const ServerSelectionState = () => {
    const selectedServer = { // placeholder
        displayName: "Tiki Phonk Server",
        rootPath: "C:\\Users\\jamil\\Desktop\\Minecraft Servers\\Tiki Phonk Server",
    }

    return (
        <div className={styles.sidebarServerState}>
            <span className={styles.sidebarStateLabel}>{selectedServer?.displayName ?? "No server selected"}</span>
            <small>{selectedServer?.rootPath ?? "Open a Minecraft server folder to begin editing"}</small>
        </div>
    )
}

export default ServerSelectionState;