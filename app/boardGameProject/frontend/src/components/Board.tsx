import React from "react";
import styles from "../styles/Board.module.css";
import { ApiGateway } from "../BoardController";
import {
  Table,
  Player,
  Piece,
  Block,
  BoardProps,
} from "../useState/BoardState";
import useBoardState from "../useState/BoardState";
import GameSetPopUp from "./GameSetPopUp";

const InitialPieceDisplay: React.FC<{
  pieces: Piece[];
  player: Player;
  handlePieceClick: Function;
  isPlayer1: boolean;
}> = ({ pieces, player, handlePieceClick, isPlayer1 }) => (
  <div className={styles.dFlex}>
    {Object.values(pieces)
      .filter((piece) => piece.owner === player.name)
      .map((piece, index) => (
        <img
          key={player.name + index}
          src={
            isPlayer1
              ? `../img/unknownGhost.jpeg`
              : `../img/${piece.type}Ghost.jpeg`
          }
          className={
            isPlayer1 ? `${styles.ghostImg} ${styles.rotate}` : styles.ghostImg
          }
          onClick={() => handlePieceClick(piece)}
          alt="piece"
        ></img>
      ))}
  </div>
);

const BoardRow: React.FC<{
  row: Block[];
  handleBlockClick: Function;
  handlePieceClick: Function;
}> = ({ row, handleBlockClick }) => (
  <div className={styles.row}>
    {row.map((square, col_i) => (
      <div
        key={"col" + col_i}
        className={styles.block}
        onClick={() => handleBlockClick(square)}
      >
        {/*
                todo
                1. square.piece.owner === "cpu"とハードコードしているのをplayers[1]に直す
                2. square.piece.ownerもisPlayer1などの変数にする
                */}
        {square.piece && (
          <img
            src={
              square.piece.owner === "cpu"
                ? `../img/unknownGhost.jpeg`
                : `../img/${square.piece.type}Ghost.jpeg`
            }
            className={
              square.piece.owner === "cpu"
                ? `${styles.ghostImgSmall} ${styles.rotate}`
                : styles.ghostImgSmall
            }
            alt="piece"
          />
        )}
      </div>
    ))}
  </div>
);

const PickedPiecesArea: React.FC<{pieces: Piece[], player: Player}> = ({pieces, player}) => (
    <div className={styles.dFlex}>
        {pieces.map((piece , index) => (
            <img key={player.name + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} alt="pickedPieces"></img>
        ))}
    </div>
);

const Board: React.FC<BoardProps> = ({ initialData, playMode}) => {
  const {
    boardInfo,
    setBoardInfo,
    playerUnsetPieces,
    players,
    setPlayers,
    handlePieceClick,
    handleBlockClick,
    isGameStarted,
    setIsGameStarted,
    turn,
    setTurn,
    isGameOver,
    setIsGameOver,
    winner,
    setWinner,
    playerPickedPieces,
  } = useBoardState(initialData, playMode);

  React.useEffect(() => {
    const allPiecesSet = playerUnsetPieces.every(
      (pieces) => pieces.length === 0
    );
    if (allPiecesSet && !isGameStarted) {
      console.log("all pieces set");
      const gameData: Table = {
        players: players,
        winner: "",
        table: boardInfo,
        turn: 0,
      };
      console.log(gameData);
      ApiGateway.notifyGetReady(gameData).then((res) => {
        setPlayers(res.players);
        setBoardInfo(res.table);
        setIsGameStarted(true);
      });
    }
  });

  React.useEffect(() => {
    if (turn === 1) {
      ApiGateway.cpuMovePiece().then((res) => {
        setPlayers(res.players);
        setBoardInfo(res.table);
        setTurn(res.turn);
        if (res.winner !== "") {
          setIsGameOver(true);
          setWinner(res.winner);
        }
      });
    }
  }, [turn, setTurn, setPlayers, setBoardInfo, setIsGameOver, setWinner]);

  return (
    <div className={styles.container}>
      <div className={styles.capturedPiecesTop}>
        {<PickedPiecesArea pieces={playerPickedPieces[1]} player={initialData.players[1]}/>}
        <InitialPieceDisplay
          pieces={playerUnsetPieces[1]}
          player={initialData.players[1]}
          handlePieceClick={handlePieceClick}
          isPlayer1={true}
        />
      </div>
      <div className={styles.board}>
        {boardInfo.map((row, row_i) => (
          <BoardRow
            key={"row" + row_i}
            row={row}
            handleBlockClick={handleBlockClick}
            handlePieceClick={handlePieceClick}
          />
        ))}
      </div>
      <div className={styles.capturedPiecesBottom}>
        <InitialPieceDisplay
          pieces={playerUnsetPieces[0]}
          player={initialData.players[0]}
          handlePieceClick={handlePieceClick}
          isPlayer1={false}
        />
        {<PickedPiecesArea pieces={playerPickedPieces[0]} player={initialData.players[0]}/>}
      </div>

      {isGameOver && <GameSetPopUp winner={winner} />}
    </div>
  );
};

export default Board;
