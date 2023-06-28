import React from "react";
import styles from "./Lobby.module.css";
import GeisterRule from "./GeisterRule";

const Lobby: React.FC = () => {
    const [showGeisterRule, setGeisterRule] = React.useState<boolean>(false);
    const [playMode, setPlayMode] = React.useState<string>("");
    const handleClick = () => {
        setGeisterRule(true);
        setPlayMode("vscpu");
    }
    return (
            showGeisterRule ? <GeisterRule playMode={playMode}/> : (
                <div className={styles.container}>
                    <div className={styles.background}>
                        <button className={styles.button} id="single-mode-btn" onClick={handleClick}>Play<br></br>(click here!)</button>
                    </div>
                </div>
            )
    )
}

export default Lobby;