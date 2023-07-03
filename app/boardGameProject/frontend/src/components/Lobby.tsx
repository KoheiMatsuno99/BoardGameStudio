import React, { useEffect } from "react";
import styles from "../styles/Lobby.module.css";
import GeisterRule from "./GeisterRule";
import { PlayContext } from "./PlayContext";

const Lobby: React.FC = () => {
  const [showGeisterRule, setGeisterRule] = React.useState<boolean>(false);
  const [playMode, setPlayMode] = React.useState<string>("");
  const playContext = React.useContext(PlayContext);

  useEffect(() => {
    if (playContext && !playContext.doesPlay) {
      setGeisterRule(false);
    }
  }, [playContext]);
  const handleClick = () => {
    setGeisterRule(true);
    setPlayMode("vscpu");
  };
  return showGeisterRule ? (
    <GeisterRule playMode={playMode} />
  ) : (
    <div className={styles.container}>
      <div className={styles.background}>
        <button
          className={styles.button}
          id="single-mode-btn"
          onClick={handleClick}
        >
          Play<br></br>(click here!)
        </button>
      </div>
    </div>
  );
};

export default Lobby;
