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
                    {initialData["players"][1]["pieces"].filter((piece: Piece) => piece.owner === initialData["players"][1]["name"]).map((piece: Piece , index: number) => (
                        <img key={initialData["players"][1]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
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
                    {initialData["players"][0]["pieces"].filter((piece: Piece) => piece.owner === initialData["players"][0]["name"]).map((piece: Piece , index: number) => (
                            <img key={initialData["players"][0]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
                        ))}
                </div>
                <div>{initialData["players"][0]["name"]}</div>
            </div>
        </div>
    )
}

export default Board;










/* 
// Pieceに選択されているかどうかのフラグを追加します
interface Piece {
    owner: string;
    type: string;
    position: number[] | null;
    selected: boolean; // selected flag
}

// ボードの各マスの状態を表現します
interface Square {
    position: number[];
    piece: Piece | null;
}

// 初期化時、全てのマスはコマが存在しない状態にします
const initialBoard: Square[][] = Array.from({ length: 8 }, (_, i) => Array.from({ length: 8 }, (_, j) => ({ position: [i, j], piece: null })));

const Board: React.FC<BoardProps> = ({ initialData }) => {
    const [board, setBoard] = React.useState(initialBoard);
    const [selectedPiece, setSelectedPiece] = React.useState<Piece | null>(null);
    const [board, setBoard] = React.useState<Square[][]>(initialBoard);
    const [playerPieces, setPlayerPieces] = React.useState<Piece[][]>([initialData["players"][0]["pieces"], initialData["players"][1]["pieces"]]);

    // コマのクリックイベントをハンドリングします
    const handlePieceClick = (piece: Piece) => {
        // コマを選択状態にします
        setSelectedPiece(piece);
        // Remove the piece from player's pieces
        setPlayerPieces(playerPieces => playerPieces.map(pieces => pieces.filter(p => p !== piece)));
    };

    // マスのクリックイベントをハンドリングします
    const handleSquareClick = (square: Square) => {
        // 選択されているコマがあれば、マスに配置します
        if (!selectedPiece) return;
        // Make sure the square is empty
        if (square.piece) return;
        // Place the selected piece on the square
        setBoard(board => board.map(row => row.map(s => s === square ? { ...s, piece: selectedPiece } : s)));
        setSelectedPiece(null);
    };

    return (
        <div className={styles.container}>
            <div className={styles.capturedPiecesTop}>
                <div>{initialData["players"][1]["name"]}</div>
                <div className={styles.dFlex}>
                    {initialData["players"][1]["pieces"].filter((piece: Piece) => piece.owner === initialData["players"][1]["name"]).map((piece: Piece , index: number) => (
                        <img key={initialData["players"][1]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
                    ))}
                </div>
            </div>
            <div className={styles.board}>
                {board.map((row, row_i) => (
                    <div key={'row' + row_i} className={styles.row}>
                        {row.map((square, col_i) => (
                            <div key={'col' + col_i} className={styles.block} onClick={() => handleSquareClick(square)}>
                                {square.piece && <img src={`../img/${square.piece.type}Ghost.jpeg`} className={styles.ghostImg} />}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
            <div className={styles.capturedPiecesBottom}>
                <div className={styles.dFlex}>
                    {initialData["players"][0]["pieces"].filter((piece: Piece) => piece.owner === initialData["players"][0]["name"]).map((piece: Piece , index: number) => (
                        <img key={initialData["players"][0]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
                    ))}
                </div>
                <div>{initialData["players"][0]["name"]}</div>
            </div>
        </div>
    )
}


*/