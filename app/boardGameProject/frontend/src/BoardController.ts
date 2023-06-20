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
        console.log("initialized");
        console.log(response);
        console.log("----------")
        return response.data;
    }
    public static async notifyGetReady(tableInfo: Table): Promise<Table>{
        //全てのコマの初期位置が確定したらコマの位置情報をサーバーに送信する          
        const response = await axios.post('http://localhost:8000/setup/',tableInfo, {withCredentials: true});
        console.log("get ready");
        console.log(response);
        console.log("----------")
        return response.data;
    }
    public static async movePiece(players: Player[], player_piece: Piece, piece_key: string , destination: Block): Promise<Table>{
        //　リクエストに送る情報としてplayersはいらないかも
        const movementInfo = {
            "players": players,
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
}