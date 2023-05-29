import React from "react";
import styles from "./Board.module.css";

interface Piece {
    owner: string;
    type: string;
    position: number[];
}

interface Block {
    address: number[];
    piece: Piece | null;
}

interface BoardProps {
    // todo: define initialData type
    initialData: any;
}

const initialBoard: Block[][] = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => ({ address: [i, j], piece: null })));

const Board: React.FC<BoardProps> = ({initialData}) => {
    const [selectedPiece, setSelectedPiece] = React.useState<Piece | null>(null);
    const [board, setBoard] = React.useState<Block[][]>(initialBoard);
    const [playerUnsetPieces, setPlayerPieces] = React.useState<Piece[][]>([initialData["players"][0]["pieces"], initialData["players"][1]["pieces"]]);
    const handlePieceClick = (piece: Piece) => {
        setSelectedPiece(piece);
        setPlayerPieces(playerUnsetPieces => playerUnsetPieces.map(pieces => pieces.filter(p => p !== piece)));
    }
    const handleBlockClick = (block: Block) => {
        if (!selectedPiece) return;
        if (block.piece) return;
        setBoard(board => board.map(row => row.map(b => b === block ? { ...b, piece: selectedPiece } : b)));
        setSelectedPiece(null);
    }
    return (
        <div className={styles.container}>
            <div className={styles.capturedPiecesTop}>
                <div>{initialData["players"][1]["name"]}</div>          
                <div className={styles.dFlex}>
                    {playerUnsetPieces[0].filter((piece: Piece) => piece.owner === initialData["players"][0]["name"]).map((piece: Piece , index: number) => (
                        <img key={initialData["players"][0]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
                    ))}
                </div>
            </div>
            <div className={styles.board}>
                {board.map((row, row_i) => (
                    <div key={'row' + row_i} className={styles.row}>
                        {row.map((square, col_i) => (
                            <div key={'col' + col_i} className={styles.block} onClick={() => handleBlockClick(square)}>
                                {square.piece && <img src={`../img/${square.piece.type}Ghost.jpeg`} className={styles.ghostImgSmall} />}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
            <div className={styles.capturedPiecesBottom}>
                <div className={styles.dFlex}>
                    {playerUnsetPieces[1].filter((piece: Piece) => piece.owner === initialData["players"][1]["name"]).map((piece: Piece , index: number) => (
                        <img key={initialData["players"][1]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
                    ))}
                </div>
                <div>{initialData["players"][0]["name"]}</div>
            </div>
        </div>
    )
}

export default Board;