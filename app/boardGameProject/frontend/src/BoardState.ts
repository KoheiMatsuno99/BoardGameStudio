import { useState } from "react";
import { ApiGateway } from "./BoardController";
import useValidateMovement from "./useValidateMovement";
import useInitialPlacement from "./useInitialPlacement";

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
        initialData,
        setBoardInfo,
        setPlayerPieces,
        setPlayers,
        setIsGameStarted,
        selectedPiece,
        setSelectedPiece,
        players,
    );

    const validateMovement = useValidateMovement();

    const handleMovement = (block: Block) => {
        if(selectedPiece === null){
            alert("コマを選択してください");
            return;
        }
        /*
        デバッグ用メッセージ 
        console.log("Selected piece: ", selectedPiece);
        console.log("Players: ", players);
        */

        //移動におけるバリデーション
        if(!validateMovement(selectedPiece, block)){
            return;
        }
        if(block.piece?.owner === selectedPiece.owner){
            alert("自分のコマがあるマスには移動できません");
            return;
        }
        // selectedPieceKeyを探す
        let selectedPieceKey: string | null = null;
        const currentPlayer = players.find(player => player.name === selectedPiece.owner);
        console.log("Current player: ", currentPlayer);
        if (currentPlayer) {
            const keys = Object.keys(currentPlayer.pieces);
            const values = Object.values(currentPlayer.pieces);
            for (let i = 0; i < keys.length; i++) {
                const value = values[i];
                if (value.owner === selectedPiece.owner && value.type === selectedPiece.type && value.position[0] === selectedPiece.position[0] && value.position[1] === selectedPiece.position[1]) {
                    selectedPieceKey = keys[i];
                    console.log("selectedPieceKey: ", selectedPieceKey);
                    break;
                }
            }
        }
        let pieceOfPositionUpdated = {...selectedPiece, position: block.address}
        setBoardInfo(board => board.map(
            row => row.map(
                b => {
                    if (b === block) return { ...b, piece:  pieceOfPositionUpdated};
                    if (b.piece === selectedPiece) return { ...b, piece: null};
                    return b;
                })));
        setPlayers(players => players.map(player => ({
            ...player,
            pieces: Object.entries(player.pieces).reduce((obj, [key, value]) => {
                obj[key] = value === selectedPiece ? pieceOfPositionUpdated : value;
                return obj;
            }, {} as {[key: string]: Piece})
        })));
        // 相手のコマを取る
        // todo イベントの判定をコマからマスにする（今の状態ではコマの画像にあたるため、イベントが発火しない）
        if(block.piece?.owner && block.piece.owner !== selectedPiece.owner){
            /*
            todo 取ったコマは自分のコマ置き場に移動（コマは再利用できないことに注意）
            */
           const newBlock = {...block, piece: selectedPiece};
           setBoardInfo(board => board.map(row => row.map(b => b === block ? newBlock : b)));
        }
        if (selectedPieceKey === null) {
            alert("あなたのコマではないので動かせません");
            setSelectedPiece(null);
            return
        }
        else{
            ApiGateway.movePiece(selectedPiece, selectedPieceKey, block)
            .then(res => {
                setPlayers(res.players);
                setBoardInfo(res.table);
                setTurn(res.turn);
            });
            setSelectedPiece(null);            
        }
    }

    const handleBlockClick = (block: Block) => {
        if(selectedPiece === null && block.piece !== null){
            handlePieceClick(block.piece);
        }
        else if(isGameStarted){
            handleMovement(block);
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