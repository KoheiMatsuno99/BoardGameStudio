import React from "react";
import styles from "./Lobby.module.css";
import GeisterRule from "./GeisterRule";

const Lobby: React.FC = () => {
    const [showGeisterRule, setGeisterRule] = React.useState<boolean>(false);
    const [isOffline, setOffline] = React.useState<boolean>(false);
    const handleClick = () => {
        setGeisterRule(true);
        setOffline(true);
    }
    return (
            showGeisterRule ? <GeisterRule isOffline={isOffline}/> : (
                <div className={styles.container}>
                    <div className={styles.background}>
                        <button className={styles.button} id="single-mode-btn" onClick={handleClick}>Play<br></br>(click here!)</button>
                    </div>
                </div>
            )
    )
}

export default Lobby;