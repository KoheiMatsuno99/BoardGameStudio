import React from "react";
import styles from "./Board.module.css";
import { ApiGateway } from "./BoardController";

const Board: React.FC = () => {
    return (
        <div className={styles.container}>
            <div className={styles.capturedPiecesTop}></div>
            <div className={styles.board}>
                {Array.from({length: 8}).map((_, row_i) => (
                    <div key={'row' + row_i} className={styles.row}>
                        {Array.from({length: 8}).map((_, col_i) => (
                            <div key={'col' + col_i} className={styles.block}></div>
                        ))}
                    </div>
                ))}
            </div>
            <div className={styles.capturedPiecesBottom}></div>
        </div>
    )
}

export default Board;