import React from "react";
import styles from "./Board.module.css";
import { ApiGateway } from "./BoardController";

interface BoardProps {
    //to do: define initialData type
    initialData: any;
}

const Board: React.FC<BoardProps> = ({initialData}) => {
    const [table, setTable] = React.useState(null);

    React.useEffect(() => {
        if(table){

        }
    }, [table])
    return (
        <div className={styles.container}>
            <div className={styles.capturedPiecesTop}>
                {initialData["players"][0]}
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
                {initialData["players"][1]}
            </div>
        </div>
    )
}

export default Board;