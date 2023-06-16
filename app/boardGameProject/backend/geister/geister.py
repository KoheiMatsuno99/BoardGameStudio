import random
from typing import Optional


class Piece:
    def __init__(
        self, owner: str, type: str, position: Optional[list[int]] = None
    ) -> None:
        self.__owner = owner
        self.__type = type
        self.__position: Optional[list[int]] = position
        assert type in {"red", "blue"}, "Type must be either 'red' or 'blue'."

    # ownerはPlayer.nameと紐づくことを想定しているが、オンラインモードで名前が衝突した時、バグの可能性あり

    def get_owner(self) -> str:
        return self.__owner

    def set_owner(self, owner: str) -> None:
        self.__owner = owner

    def get_type(self) -> str:
        return self.__type

    # Pieceのtypeは不変なのでsetterは定義しない
    def get_position(self) -> Optional[list[int]]:
        return self.__position

    # table[x][y].set_piece()と合わせて使う
    def set_position(self, position: Optional[list[int]]) -> None:
        self.__position = position

    @property
    def owner(self) -> str:
        return self.__owner

    @property
    def type(self) -> str:
        return self.__type

    @property
    def position(self) -> Optional[list[int]]:
        return self.__position


class Block:
    def __init__(self, address: list[int], piece: Optional[Piece] = None) -> None:
        if address[0] not in range(0, 8):
            raise ValueError("Address x must be in range(0, 8)")
        if address[1] not in range(0, 8):
            raise ValueError("Address y must be in range(0, 8)")
        self.__address = address
        self.__piece: Optional[Piece] = piece

    @property
    def address(self) -> list[int]:
        return self.__address

    @property
    def piece(self) -> Optional[Piece]:
        return self.__piece

    def get_address(self) -> list[int]:
        return self.__address

    # Blockに付与するaddressは不変なのでsetterは定義しない
    def set_piece(self, piece: Optional[Piece]) -> None:
        self.__piece = piece

    def get_piece(self) -> Optional[Piece]:
        return self.__piece


class Player:
    # todo オンライン対戦時に名前被りで衝突する可能性があるので、名前ではなくidに変更or追加
    # idはプレイヤーの戦績を管理するPlayerInfoクラスからとってくる
    def __init__(self, name: str, pieces: Optional[dict[str, Piece]] = None) -> None:
        self.name = name
        # pieces is Noneになるのはゲーム開始時
        if pieces is None:
            self.pieces: dict[str, Piece] = {
                f"{self.name}_blue_{i}": Piece(self.name, "blue") for i in range(4)
            }
            self.pieces.update(
                {f"{self.name}_red_{i}": Piece(self.name, "red") for i in range(4)}
            )
        # piece is not Noneの場合は位置情報を更新する場合を想定
        else:
            self.pieces = pieces
        self.__picked_red_pieces_count: int = 0
        self.__picked_blue_pieces_count: int = 0

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

    @property
    def picked_red_pieces_count(self) -> int:
        return self.__picked_red_pieces_count

    @property
    def picked_blue_pieces_count(self) -> int:
        return self.__picked_blue_pieces_count


class Table:
    def __init__(
        self, players: list[Player], table: Optional[list[list[Block]]] = None
    ) -> None:
        self.__players = players
        self.__table = (
            [[Block([x, y]) for y in range(8)] for x in range(8)]
            if table is None
            else table
        )
        self.__winner: str = ""
        self.__escapable_positions: dict[int, list[tuple[int, int]]] = {
            # self.__players[0]の逃げられる場所は[(0, 0), (0, 7)]
            0: [(0, 0), (0, 7)],
            # self.__players[1]の逃げられる場所は[(7, 0), (7, 7)]
            1: [(7, 0), (7, 7)],
        }
        self.__turn: int = 0

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def table(self) -> list[list[Block]]:
        return self.__table

    @property
    def winner(self) -> str:
        return self.__winner

    @property
    def escapable_positions(self) -> dict[int, list[tuple[int, int]]]:
        return self.__escapable_positions

    @property
    def turn(self) -> int:
        return self.__turn

    def get_players(self) -> list[Player]:
        return self.__players

    def get_table(self) -> list[list[Block]]:
        return self.__table

    def get_winner(self) -> str:
        return self.__winner

    def get_turn(self) -> int:
        return self.__turn

    def switch_turn(self) -> None:
        self.__turn = 1 if self.__turn == 0 else 0

    # CPUがコマの初期位置を決定するメソッド
    def initialize_pieces_position(self) -> None:
        for i in range(len(self.__players)):
            # オフラインモード時のCPUは初期位置をランダムに決定
            # todo プレイヤーは手動で初期位置を決定するようにする
            # todo オンラインモードでは二人のプレイヤーがそれぞれ手動で初期位置を決定する
            # todo 各プレイヤーの初期位置設定は非同期処理で行い、一方のプレイヤーが相手の配置完了まで待たないようにする
            for piece in self.__players[i].pieces.values():
                # 各コマは同じ位置には置けない
                # [0, 0]から[7, 1]までの範囲でランダムに決定
                # 8個のコマを全て置くまでループ
                while True:
                    x: int = random.randint(0, 7)
                    y: int = random.randint(0, 1) if i == 1 else random.randint(6, 7)
                    if self.__table[x][y].get_piece() is None:
                        self.__table[x][y].set_piece(piece)
                        piece.set_position([x, y])
                        break

    def get_piece_at(self, position: list[int]) -> Optional[Piece]:
        return self.__table[position[0]][position[1]].get_piece()

    # 相手の駒を奪うメソッド
    # destinationに相手の駒がある時に呼び出す
    def _pick(self, player: Player, destination: Block) -> None:
        target: Optional[Piece] = destination.get_piece()
        if target is None:
            raise ValueError("移動先に駒がありません")
        # todo destinationにある駒(target)を相手のpiecesから削除
        opponent: Player = [
            p for p in self.__players if p.get_name() != player.get_name()
        ][0]
        for key, piece in opponent.pieces.items():
            if piece == target:
                opponent.pieces.pop(key)
                break
        target.set_position(None)
        self.__table[destination.get_address()[0]][
            destination.get_address()[1]
        ].set_piece(None)
        player.add_picked_pieces_count(target)
        # 相手の青いオバケのコマを全て取ったら勝ち
        if player.get_picked_blue_pieces_count() == 4:
            print(f"{player.get_name()}は青いオバケを全て取った！")
            self.__winner = player.get_name()
        # 相手の赤いオバケのコマを全て取ったら負け（相手の勝ち）
        elif player.get_picked_red_pieces_count() == 4:
            self.__winner = opponent.get_name()

    # 自分のコマを動かすメソッド
    def move(
        self, player: Player, player_piece: Optional[Piece], destination: Block
    ) -> None:
        print("----------moving----------")
        if player_piece is None:
            raise ValueError("動かすコマを指定してください")
        if destination is None:
            raise ValueError("移動先を指定してください")
        # 仮置き オンライン対戦時に名前の衝突が起きた場合バグを生む可能性
        # この実装では脱出可能なマスにコマがある場合、次のターンで自動的に勝利になる
        if self._is_escapable(self.__turn):
            # todo 脱出されるに成功したというポップアップを出す
            print("----------escapable----------")
            self.__winner = player.get_name()
            # ここでフロントエンドと通信を行う
            return
        print("----------not escapable----------")
        # 移動先に相手のコマがあれば奪う
        target: Optional[Piece] = destination.get_piece()
        if target is not None and target.get_owner() != player_piece.get_owner():
            self._pick(player, destination)
        # 移動元のブロックからコマを削除
        current_position: Optional[list[int]] = player_piece.get_position()
        if current_position is None:
            raise ValueError("player_pieceのpositionがNoneです")
        self.__table[current_position[0]][current_position[1]].set_piece(None)
        # 移動先のブロックにコマを配置
        destination_position: list[int] = destination.get_address()
        player_piece.set_position(destination_position)
        self.__table[destination_position[0]][destination_position[1]].set_piece(
            player_piece
        )

    def _is_movable(self, piece: Piece, destination: Block) -> bool:
        # 現在位置の上下左右1マスより離れていたら移動不可
        current_position: Optional[list[int]] = piece.get_position()
        if current_position is None:
            raise ValueError("current_positionがNoneです")
        destination_position: list[int] = destination.get_address()
        x_diff: int = abs(current_position[0] - destination_position[0])
        y_diff: int = abs(current_position[1] - destination_position[1])
        if x_diff + y_diff > 1:
            return False
        # 移動しないという選択肢はなし
        if x_diff == 0 and y_diff == 0:
            return False
        target_piece = destination.get_piece()
        if target_piece is None:
            return True
        # destinationに自分のコマがある場合は移動不可
        if piece.get_owner() == target_piece.get_owner():
            print(piece.get_owner())
            print(target_piece.get_owner())
            return False
        return True

    def _is_escapable(self, turn: int) -> bool:
        for position in self.__escapable_positions[turn]:
            piece: Optional[Piece] = self.__table[position[0]][position[1]].get_piece()
            print(type(piece))
            if piece is None:
                print("piece is None")
                continue
            if (
                piece is not None
                and piece.get_owner() == self.__players[turn].get_name()
                and piece.get_type() == "blue"
            ):
                return True
        return False

    # ゲームの進行を行うメソッド
    def play(self) -> None:
        print("Game Start!")
        # 各プレイヤーがコマの初期位置を設定する
        # オフラインモードではCPUのコマは自動で設定する
        # オンラインモードでは各プレイヤーが同時に設定できるように非同期処理を使用する
        # 一方のプレイヤーが配置完了した後に、もう一方のプレイヤーが配置をするように制御するのはUXが悪い
        while self.__winner:
            for player in self.__players:
                # todo
                # not _is_movable の時はアラートと共に、
                # _is_movableになるまで再度移動場所を指定させる
                # フロントエンド実装段階ではマスをタップすることでそこにあるコマを引数pieceに渡す
                # そして、pieceを選択した状態で行き先のマスをタップするとdestinationに渡すようにする
                if self._is_movable(Piece(player.get_name(), "blue"), Block([3, 4])):
                    # piece, destinationは仮置き
                    self.move(player, Piece(player.get_name(), "blue"), Block([3, 4]))
        print("Game Set!")
        print(self.__winner + " wins!")
