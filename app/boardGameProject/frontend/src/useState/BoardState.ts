import { useState } from "react";
import useInitialPlacement from "./useInitialPlacement";
import useMovement from "./useMovement";

export interface Piece {
  owner: string;
  type: string;
  position: number[];
}

export interface Block {
  address: number[];
  piece: Piece | null;
}

export interface Player {
  name: string;
  pieces: {
    [key: string]: Piece;
  };
  pickedBluePiecesCount: number;
  pickedRedPiecesCount: number;
}

export interface Table {
  players: Player[];
  winner: string;
  table: Block[][];
  turn: number;
}

export interface BoardProps {
  initialData: Table;
  playMode: string;
}

const useBoardState = (initialData: Table, playMode: string) => {
  const isOffline = playMode === "vscpu";
  const initialBoard: Block[][] = isOffline
    ? Array.from({ length: 8 }, (_, i) =>
        Array.from({ length: 8 }, (_, j) => {
          const piece = initialData.table[i][j].piece;
          return { address: [i, j], piece: piece ? { ...piece } : null };
        })
      )
    : Array.from({ length: 8 }, (_, i) =>
        Array.from({ length: 8 }, (_, j) => {
          return { address: [i, j], piece: null };
        })
      );

  const [selectedPiece, setSelectedPiece] = useState<Piece | null>(null);
  const [boardInfo, setBoardInfo] = useState<Block[][]>(initialBoard);
  // まだ初期配置が完了していないコマを管理する
  const [playerUnsetPieces, setPlayerPieces] = useState<Piece[][]>([
    Object.values(initialData.players[0].pieces),
    isOffline ? [] : Object.values(initialData.players[1].pieces),
  ]);
  const [players, setPlayers] = useState<Player[]>(initialData.players);
  const [isGameStarted, setIsGameStarted] = useState<boolean>(false);
  const [turn, setTurn] = useState<number>(initialData.turn);
  const [playerPickedPieces, setPlayerPickedPieces] = useState<Piece[][]>([
    [],
    [],
  ]);
  const [isGameOver, setIsGameOver] = useState<boolean>(false);
  const [winner, setWinner] = useState<string>("");

  const handlePieceClick = (piece: Piece) => {
    if (isGameStarted && players[turn].name !== piece.owner) {
      alert(`今は${players[turn].name}のターンです`);
      return;
    }
    setSelectedPiece(piece);
    console.log("Piece Selected!");
  };

  const handleInitialPlacement = useInitialPlacement(
    setBoardInfo,
    setPlayerPieces,
    setPlayers,
    setSelectedPiece,
    players
  );

  const handleMovement = useMovement(
    players,
    setPlayers,
    setSelectedPiece,
    setBoardInfo,
    setTurn,
    setIsGameOver,
    setWinner,
    playerPickedPieces,
    setPlayerPickedPieces
  );

  const handleBlockClick = (block: Block) => {
    if (selectedPiece === null && block.piece !== null) {
      handlePieceClick(block.piece);
    } else if (selectedPiece === null) {
      alert("コマを選択してください");
      return;
    } else if (isGameStarted) {
      // 呼び出し先でselectedPieceのnullチェックを行うので!で問題なし
      handleMovement(selectedPiece!, block);
    } else {
      // 呼び出し先でselectedPieceのnullチェックを行うので!で問題なし
      handleInitialPlacement(selectedPiece!, block);
    }
  };
  return {
    setSelectedPiece,
    boardInfo,
    setBoardInfo,
    playerUnsetPieces,
    setPlayerPieces,
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
    playerPickedPieces
  };
};

export default useBoardState;
