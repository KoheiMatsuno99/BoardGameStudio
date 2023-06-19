import React from "react";
import styles from "./Board.module.css";
import { ApiGateway } from "./BoardController";
import { Table, Player, Piece, Block, BoardProps } from "./BoardState";
import useBoardState from "./BoardState";

const PieceDisplay: React.FC<{pieces: Piece[], player: Player, handlePieceClick: Function}> = ({pieces, player, handlePieceClick}) => (
    <div className={styles.dFlex}>
        {Object.values(pieces).filter(piece => piece.owner === player.name).map((piece , index) => (
            <img key={player.name + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg} onClick={() => handlePieceClick(piece)}></img>
        ))}
    </div>
);

const BoardRow: React.FC<{row: Block[], handleBlockClick: Function, handlePieceClick: Function}> = ({row, handleBlockClick, handlePieceClick}) => (
    <div className={styles.row}>
        {row.map((square, col_i) => (
            <div key={'col' + col_i} className={styles.block} onClick={() => handleBlockClick(square)}>
                {square.piece && <img src={`../img/${square.piece.type}Ghost.jpeg`} className={styles.ghostImgSmall} onClick={
                    (event) => {
                        event.stopPropagation();
                        handlePieceClick(square.piece);
                    }
                }/>}
            </div>
        ))}
    </div>
);

const Board: React.FC<BoardProps> = ({initialData}) => {
    const {
        selectedPiece,
        boardInfo,
        playerUnsetPieces,
        players,
        handlePieceClick,
        handleBlockClick,
        isGameStarted,
        setIsGameStarted
    } = useBoardState(initialData);

    React.useEffect(() => {
        const allPiecesSet = playerUnsetPieces.every(pieces => pieces.length === 0);
        if (allPiecesSet && !isGameStarted){
            console.log('all pieces set')
            const gameData: Table = {
                players: players,
                winner: "",
                table: boardInfo,
                turn: 0
            }
            console.log(gameData);
            ApiGateway.notifyGetReady(gameData);
            setIsGameStarted(true);
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
                    <BoardRow key={'row' + row_i} row={row} handleBlockClick={handleBlockClick} handlePieceClick={handlePieceClick}/>
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
