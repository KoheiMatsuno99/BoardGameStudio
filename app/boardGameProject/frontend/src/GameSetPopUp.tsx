import React from "react";
import Lobby from "./Lobby";
import styles from "./GameSetPopUp.module.css";

interface GameSetPopUpProps {
    winner: string;
    //onGameEnd: () => void;
}

const GameSetPopUp: React.FC<GameSetPopUpProps> = (GameSetPopUpProps) => {
    const [doesEndGame, setEndGame] = React.useState(false);
    const handleEndGame = () => {
        setEndGame(true);
    }
    if (doesEndGame){
        return <Lobby />
    }
    return (
        <div className={styles.container}>
            <h1 className={styles.text}>winner: {GameSetPopUpProps.winner}</h1>
            <div>
                <button onClick={handleEndGame}>Home</button>
            </div>
        </div>
    )
}

export default GameSetPopUp;