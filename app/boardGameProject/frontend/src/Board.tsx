import React from "react";
import styles from "./Board.module.css";

interface Piece {
    owner: string;
    type: string;
    position: number[];
}

interface BoardProps {
    // todo: define initialData type
    initialData: any;
}

const Board: React.FC<BoardProps> = ({initialData}) => {
    return (
        <div className={styles.container}>
            <div className={styles.capturedPiecesTop}>
                <div>{initialData["players"][1]["name"]}</div>          
                <div className={styles.dFlex}>
                    {initialData["players"][1]["pieces"].filter((piece: Piece) => piece.owner === initialData["players"][1]["name"]).map((piece: Piece , index: number) => (
                        <img key={initialData["players"][1]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg}></img>
                    ))}
                </div>
            </div>
            <div className={styles.board}>
                {Array.from({length: 8}).map((_, row_i) => (
                    <div key={'row' + row_i} className={styles.row}>
                        {Array.from({length: 8}).map((_, col_i) => (
                            <div key={'col' + col_i} className={styles.block}></div>
                        ))}
                    </div>
                ))}
            </div>
            <div className={styles.capturedPiecesBottom}>
                <div className={styles.dFlex}>
                    {initialData["players"][0]["pieces"].filter((piece: Piece) => piece.owner === initialData["players"][0]["name"]).map((piece: Piece , index: number) => (
                            <img key={initialData["players"][0]["name"] + index} src={`../img/${piece.type}Ghost.jpeg`} className={styles.ghostImg}></img>
                        ))}
                </div>
                <div>{initialData["players"][0]["name"]}</div>
            </div>
        </div>
    )
}

export default Board;