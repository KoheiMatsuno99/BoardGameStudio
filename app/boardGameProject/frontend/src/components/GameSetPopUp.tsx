import React from "react";
import Lobby from "./Lobby";
import styles from "../styles/GameSetPopUp.module.css";
import { PlayContext } from "./PlayContext";

interface GameSetPopUpProps {
  winner: string;
}

const GameSetPopUp: React.FC<GameSetPopUpProps> = (GameSetPopUpProps) => {
  const [doesEndGame, setEndGame] = React.useState(false);
  const playContext = React.useContext(PlayContext);

  const handleEndGame = () => {
    setEndGame(true);
    if (playContext) {
      playContext.setDoesPlay(false);
    }
  };
  if (doesEndGame && playContext && !playContext.doesPlay) {
    return <Lobby />;
  }
  return (
    <div className={styles.container}>
      <h1 className={styles.text}>winner: {GameSetPopUpProps.winner}</h1>
      <div>
        <button onClick={handleEndGame}>Home</button>
      </div>
    </div>
  );
};

export default GameSetPopUp;
