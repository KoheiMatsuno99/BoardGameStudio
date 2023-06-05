import { useState } from "react";

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
    pieces: Piece[];
}

export interface Table{
    players: Player[],
    winner: string,
    table: Block[][]
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
    const [playerUnsetPieces, setPlayerPieces] = useState<Piece[][]>([initialData.players[0].pieces, initialData.players[1].pieces]);
    const [players, setPlayers] = useState<Player[]>(initialData.players);

    const handlePieceClick = (piece: Piece) => {
        setSelectedPiece(piece);
    }

    const handleBlockClick = (block: Block) => {
        if (!selectedPiece) return;
        if (block.piece) return;
        const playerIndex = players.findIndex(player => player.name === selectedPiece.owner);
        const validPlacementRange = [
            {"rowStart": 0, "rowEnd": 1, "colStart": 0, "colEnd": 7},
            {"rowStart": 6, "rowEnd": 7, "colStart": 0, "colEnd": 7},
        ]
        const {rowStart, rowEnd, colStart, colEnd} = validPlacementRange[playerIndex]
        const [selectedRow, selectedCol] = block.address;
        if(selectedRow < rowStart || selectedRow > rowEnd || selectedCol < colStart || selectedCol > colEnd){
            alert("初期位置は手前の2行の範囲にコマを置いてください");
            return;
        }
        else if(playerIndex === 0 && selectedRow === rowStart && (selectedCol === colStart || selectedCol === colEnd)){
            alert("相手プレイヤーの脱出マスを初期位置に設定することはできません")
            return;
        }
        else if(playerIndex === 1 && selectedRow === rowEnd && (selectedCol === colStart || selectedCol === colEnd)){
            alert("相手プレイヤーの脱出マスを初期位置に設定することはできません")
            return;
        }
        let pieceOfPositionUpdated = {...selectedPiece, position: block.address}
        setBoardInfo(board => board.map(row => row.map(b => b === block ? { ...b, piece:  pieceOfPositionUpdated} : b)));
        setPlayerPieces(playerUnsetPieces => playerUnsetPieces.map(pieces => pieces.filter(p => p !== selectedPiece)));
        setPlayers(players => players.map(player => ({
            ...player,
            pieces: player.pieces.map(piece => piece === selectedPiece ? pieceOfPositionUpdated : piece)
        })));
        setSelectedPiece(null);
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
        handleBlockClick
    };
};

export default useBoardState;