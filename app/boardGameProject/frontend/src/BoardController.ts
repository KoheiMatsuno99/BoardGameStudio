import {Table, Player, Piece, Block} from './BoardState';
import axios from 'axios';

export class ApiGateway{
    public static async initializeGame(player1: string, player2: string): Promise<Table>{
        const playerData = [
            {
                "name": player1,
            },
            {
                "name": player2,
            }
        ];
        //todo リクエスト先をlocalhostから変更する
        const response = await axios.post('http://localhost:8000/start/', playerData, { withCredentials: true })
        /* 
        デバッグ用メッセージ
        console.log("initialized");
        console.log(response);
        console.log("----------");
        */

        return response.data;
    }
    public static async notifyGetReady(tableInfo: Table): Promise<Table>{
        //全てのコマの初期位置が確定したらコマの位置情報をサーバーに送信する          
        const response = await axios.post('http://localhost:8000/setup/',tableInfo, {withCredentials: true});
        /*
        デバッグ用メッセージ
        console.log("get ready");
        console.log(response);
        console.log("----------");
        */
        
        return response.data;
    }
    public static async movePiece(player_piece: Piece, piece_key: string , destination: Block): Promise<Table>{
        //　リクエストに送る情報としてplayersはいらないかも
        const movementInfo = {
            "player_piece": player_piece,
            "piece_key": piece_key,
            "destination": destination
        }
        const response = await axios.post('http://localhost:8000/movement/', movementInfo, {withCredentials: true});
        console.log("moved");
        console.log(response);
        console.log("----------");
        return response.data;
    }
    public static async cpuMovePiece(): Promise<Table>{
        const response = await axios.post('http://localhost:8000/cpu-movement/',{},{withCredentials: true});
        console.log("cpu moved");
        console.log(response);
        console.log("----------");
        return response.data;
    }
}