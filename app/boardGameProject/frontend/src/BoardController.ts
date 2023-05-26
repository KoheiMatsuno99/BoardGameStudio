import axios from 'axios';
export class ApiGateway{
    public static async initializeGame(player1: string, player2: string){
        const playerData = [
            {"name": player1},
            {"name": player2}
        ];
        //todo リクエスト先をlocalhostから変更する
        const response = await axios.post('http://localhost:8000/start_game/', playerData);
        return response.data;
    }
    public static async movePiece(player: string, player_piece: string, destination: string){
        
    }
}