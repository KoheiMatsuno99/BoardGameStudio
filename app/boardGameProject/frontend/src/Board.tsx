import React, { useState } from "react";
import styles from "./Board.module.css";
import { ApiGateway } from "./BoardController";

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
    initialData: any;
}

const initialBoard: Block[][] = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => ({ address: [i, j], piece: null })));

const PieceDisplay: React.FC<{pieces: Piece[], player: Player, handlePieceClick: Function}> = ({pieces, player, handlePieceClick}) => (
    <div className={styles.dFlex}>
        {pieces.filter(piece => piece.owner === player.name).map((piece , index) => (
            <img key={player.name + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
        ))}
    </div>
);

const BoardRow: React.FC<{row: Block[], handleBlockClick: Function}> = ({row, handleBlockClick}) => (
    <div className={styles.row}>
        {row.map((square, col_i) => (
            <div key={'col' + col_i} className={styles.block} onClick={() => handleBlockClick(square)}>
                {square.piece && <img src={`../img/${square.piece.type}Ghost.jpeg`} className={styles.ghostImgSmall} />}
            </div>
        ))}
    </div>
);

const Board: React.FC<BoardProps> = ({initialData}) => {
    const [selectedPiece, setSelectedPiece] = useState<Piece | null>(null);
    const [boardInfo, setBoardInfo] = useState<Block[][]>(initialBoard);
    const [playerUnsetPieces, setPlayerPieces] = useState<Piece[][]>([initialData.players[0].pieces, initialData.players[1].pieces]);

    const handlePieceClick = (piece: Piece) => {
        setSelectedPiece(piece);
    }

    const handleBlockClick = (block: Block) => {
        if (!selectedPiece) return;
        if (block.piece) return;
        let pieceOfPositionUpdated = {...selectedPiece, position: block.address}
        setBoardInfo(board => board.map(row => row.map(b => b === block ? { ...b, piece:  pieceOfPositionUpdated} : b)));
        setPlayerPieces(playerUnsetPieces => playerUnsetPieces.map(pieces => pieces.filter(p => p !== selectedPiece)));
        setSelectedPiece(null);
    }

    React.useEffect(() => {
        const allPiecesSet = playerUnsetPieces.every(pieces => pieces.length === 0);
        if (allPiecesSet){
            console.log('all pieces set')
            console.log(boardInfo)
            ApiGateway.notifyGetReady(boardInfo);
        }
    })

    return (
        <div className={styles.container}>
            <div className={styles.capturedPiecesTop}>
                <div>{initialData.players[1].name}</div>          
                <PieceDisplay pieces={playerUnsetPieces[0]} player={initialData.players[0]} handlePieceClick={handlePieceClick} />
            </div>
            <div className={styles.board}>
                {boardInfo.map((row, row_i) => (
                    <BoardRow key={'row' + row_i} row={row} handleBlockClick={handleBlockClick} />
                ))}
            </div>
            <div className={styles.capturedPiecesBottom}>
                <PieceDisplay pieces={playerUnsetPieces[1]} player={initialData.players[1]} handlePieceClick={handlePieceClick} />
                <div>{initialData.players[0].name}</div>
            </div>
        </div>
    )
}

export default Board;
