class Piece:
    def __init__(self, OWNER: str, TYPE: str) -> None:
        self.__owner = OWNER
        self.__type = TYPE
        self.__position = None
        assert TYPE in {"red", "blue"} , "Type must be either 'red' or 'blue'."
    # ownerはPlayer.nameと紐づくことを想定しているが、オンラインモードで名前が衝突した時、バグの可能性あり
    def get_owner(self) -> str:
        return self.__owner
    def set_owner(self, owner: str) -> None:
        self.__owner = owner
    def get_type(self) -> str:
        return self.__type
    # Pieceのtypeは不変なのでsetterは定義しない
    def get_position(self) -> list[int]:
        # None制御
        assert type(self.__position) == list[int], "Position is not set."
        return self.__position
    def set_position(self, position: list[int]) -> None:
        self.__position = position
    def set_position_None(self) -> None:
        self.__position = None

class Block:
    def __init__(self, ADDRESS: list[int]) -> None:
        self.__address = ADDRESS
        self.__piece = None
    
    def get_address(self) -> list[int]:
        return self.__address
    # Blockに付与するaddressは不変なのでsetterは定義しない
    def set_piece(self, piece: Piece) -> None:
        self.__piece = piece
    def get_piece(self) -> Piece or None:
        return self.__piece
    # 四隅のマスは脱出可能なマスとする
    def is_escape_block(self) -> bool:
        # todo より良い書き方があれば修正
        # 8✖️8のボードを想定
        return self.__address == [0, 0] or self.__address == [0, 7] or self.__address == [7, 0] or self.__address == [7, 7]

class Player:
    __picked_red_pieces_count: int = 0
    __picked_blue_pieces_count: int = 0
    # todo オンライン対戦時に名前被りで衝突する可能性があるので、名前ではなくidに変更or追加
    # idはプレイヤーの戦績を管理するPlayerInfoクラスからとってくる 
    def __init__(self, name: str) -> None:
        self.name = name
        self.pieces: dict[str, Piece] = {
            f'{self.name}_blue_{i}': Piece(self.name, "blue") for i in range(4) 
        }
        self.pieces.update({f'{self.name}_red_{i}': Piece(self.name, "red") for i in range(4)})

    def get_name(self) -> str:
        return self.name
    def get_picked_red_pieces_count(self) -> int:
        return self.__picked_red_pieces_count
    def get_picked_blue_pieces_count(self) -> int:
        return self.__picked_blue_pieces_count
    def add_picked_pieces_count(self, piece: Piece) -> None:
        piece_type: str = piece.get_type()
        # 引数がPieceクラスのインスタンスなので、
        # 文字列は"blue"または"red"のみ考慮すれば良い
        if piece_type == "blue":
            self.__picked_blue_pieces_count += 1
            print("青いオバケを奪った！")
        else:
            self.__picked_red_pieces_count += 1
            print("赤いオバケを取ってしまった...。")
    
class Table:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.table: list[list[Block]] = [[Block([x, y]) for y in range(8)] for x in range(8)]
        self.__winner: str = ""

    def get_winner(self) -> str:
        return self.__winner 
    # 相手の駒を奪うメソッド
    # destinationに相手の駒がある時に呼び出す
    def _pick(self, player: Player, destination: Block) -> None:
        target: Piece = destination.get_piece()
        # todo destinationにある駒(target)を相手のpiecesから削除 
        opponent: Player = [p for p in self.players if p.get_name() != player.get_name()][0]
        for key, piece in opponent.pieces.items():
            if piece == target:
                opponent.pieces.pop(key)
                break
        target.set_position_None()
        player.add_picked_pieces_count(target)
        # 相手の青いオバケのコマを全て取ったら勝ち
        if player.get_picked_blue_pieces_count == 4:
            self.__winner = player.get_name()
        # 相手の赤いオバケのコマを全て取ったら負け（相手の勝ち）
        elif player.get_picked_red_pieces_count == 4:
            self.__winner = opponent.get_name()

    # 自分のコマを動かすメソッド
    def move(self, player: Player, player_piece: Piece, destination: Block) -> None:
        # 仮置き オンライン対戦時に名前の衝突が起きた場合バグを生む可能性        
        assert player_piece.get_owner == player.get_name(), "Only YOUR piece can move."
        # 青いオバケの現在位置が脱出マスでdestinationも脱出マスであれば勝利
        if player_piece.get_type() == "blue":
            if destination.is_escape_block() and player_piece.get_position() == destination.get_address():
                self.__winner = player.get_name()
                return 
        if destination.get_piece is not None and destination.get_piece().get_owner() != player_piece.get_owner():
            self._pick(player, destination)
        player_piece.set_position(destination.get_address())
        destination.set_piece(player_piece)
    
    def _is_movable(self, piece: Piece, destination: Block) -> bool:
        # 現在位置の上下左右1マスより離れていたら移動不可
        current_position: list[int] = piece.get_position()
        destination_position: list[int] = destination.get_address()
        x_diff: int = abs(current_position[0] - destination_position[0])
        y_diff: int = abs(current_position[1] - destination_position[1])
        if x_diff > 1 and y_diff > 1:
            return False
        # 移動しないという選択肢はなし(青いオバケが脱出する場合は例外)
        if x_diff == 0 and y_diff == 0 and not (destination.is_escape_block() and piece.get_type() == "blue"):
            return False
        # destinationに自分のコマがある場合は移動不可
        if piece.get_owner() == destination.get_piece().get_owner():
            return False
        return True

    #ゲームの進行を行うメソッド
    def play(self) -> None:
        print("Game Start!")
        # 各プレイヤーがコマの初期位置を設定する
        # オフラインモードではCPUのコマは自動で設定する
        # オンラインモードでは各プレイヤーが同時に設定できるように非同期処理を使用する
        # 一方のプレイヤーが配置完了した後に、もう一方のプレイヤーが配置をするように制御するのはUXが悪い
        while(self.__winner):
            for player in self.players:
                # todo 
                # not _is_movable の時はアラートと共に、
                # _is_movableになるまで再度移動場所を指定させる
                # フロントエンド実装段階ではマスをタップすることでそこにあるコマを引数pieceに渡す
                # そして、pieceを選択した状態で行き先のマスをタップするとdestinationに渡すようにする                
                if self._is_movable:
                    # piece, destinationは仮置き
                    self.move(player, Piece(player.get_name(), "blue"), Block(3, 4))
        print("Game Set!")
        print(self.__winner + " wins!")