import React from "react";
import styles from "./Lobby.module.css";

const Lobby: React.FC = () => {
    return (
        <div className={styles.container}>
            <div className={styles.background}>
                <button className={styles.button} id="single-mode-btn">Single Mode</button>
            </div>  
        </div>
    )
}

export default Lobby;