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
    }
    pickedBluePiecesCount: number,
    pickedRedPiecesCount: number
}

export interface Table{
    players: Player[],
    winner: string,
    table: Block[][],
    turn: number
}

export interface BoardProps {
    initialData: Table;
}

const useBoardState = (initialData: Table) => {
    const initialBoard: Block[][] = Array.from(
        { length: 8 }, (_, i) => 
        Array.from({ length: 8 }, (_, j) => 
        ({ address: [i, j], piece: null }))
        );
    const [selectedPiece, setSelectedPiece] = useState<Piece | null>(null);
    const [boardInfo, setBoardInfo] = useState<Block[][]>(initialBoard);
    // まだ初期配置が完了していないコマを管理する
    const [playerUnsetPieces, setPlayerPieces] = useState<Piece[][]>([Object.values(initialData.players[0].pieces), Object.values(initialData.players[1].pieces)]);
    const [players, setPlayers] = useState<Player[]>(initialData.players);
    const [isGameStarted, setIsGameStarted] = useState<boolean>(false);
    const [turn, setTurn] = useState<number>(initialData.turn);
    const [playerPickedPieces, setPlayerPickedPieces] = useState<Piece[][]>([[], []]);

    const handlePieceClick = (piece: Piece) => {
        if(isGameStarted && players[turn].name !== piece.owner){
            alert(`今は${players[turn].name}のターンです`);
            return;
        }
        setSelectedPiece(piece);
        console.log("Piece Selected!")
    }

    const handleInitialPlacement = useInitialPlacement(
        setBoardInfo,
        setPlayerPieces,
        setPlayers,
        setSelectedPiece,
        players,
    );

    const handleMovement = useMovement(
        players,
        setPlayers,
        selectedPiece,
        setSelectedPiece,
        boardInfo,
        setBoardInfo,
        turn,
        setTurn
    );

    const handleBlockClick = (block: Block) => {
        if(selectedPiece === null && block.piece !== null){
            handlePieceClick(block.piece);
        }
        else if(isGameStarted){
            // 呼び出し先でselectedPieceのnullチェックを行うので!で問題なし
            handleMovement(selectedPiece!, block);
        }
        else{
            // 呼び出し先でselectedPieceのnullチェックを行うので!で問題なし
            handleInitialPlacement(selectedPiece!, block);
        }
    }
    return {
        selectedPiece,
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
        setTurn
    };
};

export default useBoardState;