import { useState } from "react";
import {Table, Player, Piece, Block} from './BoardState';

const useInitialPlacement = (
    initialData: Table,
    setBoardInfo: React.Dispatch<React.SetStateAction<Block[][]>>,
    setPlayerPieces: React.Dispatch<React.SetStateAction<Piece[][]>>,
    setPlayers: React.Dispatch<React.SetStateAction<Player[]>>,
    setIsGameStarted: React.Dispatch<React.SetStateAction<boolean>>,
    selectedPiece: Piece | null,
    setSelectedPiece: React.Dispatch<React.SetStateAction<Piece | null>>,
    players: Player[],
) => {
    const validateInitialPlacement = (selectedPiece: Piece, block: Block) => {
        if (!selectedPiece){
            alert("コマを選択してください");
            return false;
        }
        if (block.piece){
            alert("そのマスにはコマがすでに存在します");
            return false;
        }
        const playerIndex = players.findIndex(player => player.name === selectedPiece.owner);
        if(playerIndex === -1){
            alert("そのコマはすでに配置されています。残りのコマを配置してください。");
            return false;
        }
        if (selectedPiece.position !== null){
            alert("そのコマはすでに配置されています。残りのコマを配置してください。");
            return false;
        }
        const validPlacementRange = [
            {"rowStart": 6, "rowEnd": 7, "colStart": 0, "colEnd": 7},
            {"rowStart": 0, "rowEnd": 1, "colStart": 0, "colEnd": 7},
        ]
        const {rowStart, rowEnd, colStart, colEnd} = validPlacementRange[playerIndex]
        const [selectedRow, selectedCol] = block.address;
        if(selectedRow < rowStart || selectedRow > rowEnd || selectedCol < colStart || selectedCol > colEnd){
            alert("初期位置は手前の2行の範囲にコマを置いてください");
            return false;
        }
        else if(playerIndex === 0 && selectedRow === rowEnd && (selectedCol === colStart || selectedCol === colEnd)){
            alert("相手プレイヤーの脱出マスを初期位置に設定することはできません")
            return false;
        }
        else if(playerIndex === 1 && selectedRow === rowStart && (selectedCol === colStart || selectedCol === colEnd)){
            alert("相手プレイヤーの脱出マスを初期位置に設定することはできません")
            return false;
        }
        return true;
    }
    const piecePlace = (selectedPiece: Piece, block: Block) => {
        let pieceOfPositionUpdated = {...selectedPiece, position: block.address}
        setBoardInfo(board => board.map(row => row.map(b => b === block ? { ...b, piece:  pieceOfPositionUpdated} : b)));
        setPlayerPieces(playerUnsetPieces => playerUnsetPieces.map(pieces => Object.values(pieces).filter(p => p !== selectedPiece)));
        setPlayers(players => players.map(player => ({
            ...player,
            pieces: Object.entries(player.pieces).reduce((obj, [key, value]) => {
                obj[key] = value === selectedPiece ? pieceOfPositionUpdated : value;
                return obj;
            }, {} as {[key: string]: Piece})
        })));
        setSelectedPiece(null);
    }
    const initialPlacement = (selectedPiece: Piece, block: Block) => {
        if (!validateInitialPlacement(selectedPiece, block)){
            return;
        }
        const pieceOfPositionUpdated = piecePlace(selectedPiece, block);
        return pieceOfPositionUpdated;
    }
    return initialPlacement;
}

export default useInitialPlacement;
