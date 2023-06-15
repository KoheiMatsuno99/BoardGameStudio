import {Table, Player, Piece, Block} from './BoardState';
import axios from 'axios';

export class ApiGateway{
    public static async initializeGame(player1: string, player2: string): Promise<Table>{
        const playerData = [
            {
                "name": player1,
                //"picked_blue_pieces_count": 0,
                //"picked_red_pieces_count": 0, 
            },
            {
                "name": player2,
                //"picked_blue_pieces_count": 0,
                //"picked_red_pieces_count": 0,
            }
        ];
        //todo リクエスト先をlocalhostから変更する
        const response = await axios.post('http://localhost:8000/start/', playerData, { withCredentials: true })
        return response.data;
    }
    public static async notifyGetReady(tableInfo: Table): Promise<Table>{
        //全てのコマの初期位置が確定したらコマの位置情報をサーバーに送信する          
        const response = await axios.post('http://localhost:8000/setup/',tableInfo, {withCredentials: true});
        console.log(response)
        return response.data;
    }
    public static async movePiece(players: Player[], player_piece: Piece, destination: Block): Promise<Table>{
        const movementInfo = {
            "players": players,
            "player_piece": player_piece,
            "destination": destination
        }
        const response = await axios.post('http://localhost:8000/movement/', movementInfo, {withCredentials: true});
        return response.data;
    }
}