import axios from 'axios';
export class ApiGateway{
    public static async initializeGame(player1: string, player2: string){
        const playerData = [
            {"player1": player1},
            {"player2": player2}
        ];
        const response = await axios.post('/api/start_game', playerData);
    }
    public static async movePiece(player: string, player_piece: string, destination: string){
        
    }
}