import {Block} from './Board';
import axios from 'axios';

export class ApiGateway{
    public static async initializeGame(player1: string, player2: string){
        const playerData = [
            {
                "name": player1,
                "picked_blue_pieces_count": 0,
                "picked_red_pieces_count": 0
            },
            {
                "name": player2,
                "picked_blue_pieces_count": 0,
                "picked_red_pieces_count": 0
            }
        ];
        //todo リクエスト先をlocalhostから変更する
        const response = await axios.post('http://localhost:8000/start/', playerData, { withCredentials: true })
        return response.data;
    }
    public static async notifyGetReady(boardInfo: Block[][]){
        //全てのコマの初期位置が確定したらコマの位置情報をサーバーに送信する          
        const response = await axios.post('http://localhost:8000/setup/',boardInfo, {withCredentials: true});
        console.log(response)
        return response.data;
    }
    public static async movePiece(player: string, player_piece: string, destination: string){
        
    }
}