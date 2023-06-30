import random
from typing import Optional, Tuple


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
    def __init__(
        self,
        name: str,
        pieces: Optional[dict[str, Piece]] = None,
        picked_red_pieces_count: int = 0,
        piecked_blue_pieces_count: int = 0,
    ) -> None:
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
        self.__picked_red_pieces_count: int = picked_red_pieces_count
        self.__picked_blue_pieces_count: int = piecked_blue_pieces_count

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

    def get_pieces(self) -> dict[str, Piece]:
        return self.pieces

    @property
    def picked_red_pieces_count(self) -> int:
        return self.__picked_red_pieces_count

    @property
    def picked_blue_pieces_count(self) -> int:
        return self.__picked_blue_pieces_count


class Table:
    def __init__(
        self,
        players: list[Player],
        table: Optional[list[list[Block]]] = None,
        turn: int = 0,
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
        self.__turn: int = turn

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
        print(f"次は{self.__turn} {self.__players[self.__turn].get_name()}のターン")

    # CPUがコマの初期位置を決定するメソッド
    def initialize_cpu_pieces_position(self) -> None:
        # オフラインモード時のCPUは初期位置をランダムに決定
        # todo プレイヤーは手動で初期位置を決定するようにする
        # todo オンラインモードでは二人のプレイヤーがそれぞれ手動で初期位置を決定する
        # todo 各プレイヤーの初期位置設定は非同期処理で行い、一方のプレイヤーが相手の配置完了まで待たないようにする
        for piece in self.__players[1].pieces.values():
            # 各コマは同じ位置には置けない
            # 8個のコマを全て置くまでループ
            while True:
                x: int = random.randint(0, 7)
                y: int = random.randint(0, 1)
                if self.__table[y][x].get_piece() is None and (
                    not (x == 0 and y == 0) and not (x == 7 and y == 0)
                ):
                    self.__table[y][x].set_piece(piece)
                    piece.set_position([y, x])
                    break

    def get_piece_at(self, position: list[int]) -> Optional[Piece]:
        return self.__table[position[0]][position[1]].get_piece()

    # 相手の駒を奪うメソッド
    # destinationに相手の駒がある時に呼び出す
    def pick(self, destination: Block, target: Piece) -> None:
        # todo destinationにある駒(target)を相手のpiecesから削除
        player: Player = self.__players[self.__turn]
        opponent: Player = [
            p for p in self.__players if p.get_name() != player.get_name()
        ][0]
        key_to_remove: str = ""
        for key, piece in opponent.pieces.items():
            if (
                piece.get_owner() == target.get_owner()
                and piece.get_type() == target.get_type()
                and piece.get_position() == target.get_position()
            ):
                key_to_remove = key
                print(f"{player.get_name()}は{opponent.get_name()}のコマ{key}を取った！")
                break

        if key_to_remove == "":
            raise Exception("相手のコマが見つかりませんでした")
        else:
            print("key_to_remove", key_to_remove)
            opponent.pieces.pop(key_to_remove)
            print(opponent.pieces)

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
        self,
        player_piece: Optional[Piece],
        piece_key: str,
        destination: Block,
    ) -> None:
        if player_piece is None:
            raise ValueError("動かすコマを指定してください")
        if destination is None:
            raise ValueError("移動先を指定してください")
        # 仮置き オンライン対戦時に名前の衝突が起きた場合バグを生む可能性
        # この実装では脱出可能なマスにコマがある場合、次のターンで自動的に勝利になる
        if self._is_escapable(self.__turn):
            # todo 脱出に成功したというポップアップを出す
            # print("----------escapable----------")
            self.__winner = self.__players[self.__turn].get_name()
            # ここでフロントエンドと通信を行う
            # 通信を行うのはviews.pyの役割なのでモデルからは直接通信しないこと
            # ここで関数を抜けるとviews.pyに戻り、そこで通信を行う
            return

        # 移動元のブロックからコマを削除
        current_position: Optional[list[int]] = player_piece.get_position()
        if current_position is None:
            raise ValueError("player_pieceのpositionがNoneです")
        selected_piece: Optional[Piece] = self.__table[current_position[0]][
            current_position[1]
        ].get_piece()
        if selected_piece is None:
            raise ValueError("移動元のブロックにコマがありません")
        print("移動元のコマの所有者", selected_piece.get_owner())
        print("移動元のコマの種類", selected_piece.get_type())
        print(
            "移動元のアドレス",
            self.__table[current_position[0]][current_position[1]].get_address(),
        )
        self.__table[current_position[0]][current_position[1]].set_piece(None)
        # 移動先のブロックにコマを配置
        destination_position: list[int] = destination.get_address()
        player_piece.set_position(destination_position)
        self.get_players()[self.__turn].get_pieces()[piece_key].set_position(
            destination_position
        )
        self.__table[destination_position[0]][destination_position[1]].set_piece(
            player_piece
        )
        moved_piece: Optional[Piece] = self.__table[destination_position[0]][
            destination_position[1]
        ].get_piece()
        if moved_piece is None:
            raise ValueError("移動先のブロックにコマがありません")
        print("移動先のコマの所有者", moved_piece.get_owner())
        print("移動先のコマの種類", moved_piece.get_type())
        print(
            "移動先のアドレス",
            self.__table[destination_position[0]][
                destination_position[1]
            ].get_address(),
        )

    def cpu_move(self) -> None:
        print("----------cpu_move----------")
        # cpuのコマを選択
        while True:
            piece_key: str = ""
            if self.__players[1].get_picked_red_pieces_count() < 3:
                (
                    piece_key,
                    cpu_piece,
                    destination,
                    does_capture,
                ) = self._search_oppenent_blue_piece()
            else:
                cpu_piece = random.choice(list(self.__players[1].pieces.values()))
                destination_x: int = random.randint(0, 7)
                destination_y: int = random.randint(0, 7)
                destination = self.__table[destination_y][destination_x]
            # 赤だったら前に出す
            if (
                not does_capture
                and cpu_piece.get_type() == "red"
                and destination.get_address()[0] <= 6
            ):
                destination = self.__table[destination.get_address()[0] + 1][
                    destination.get_address()[1]
                ]

            if self.is_movable(cpu_piece, destination):
                break

        if piece_key == "":
            for piece_k, piece_v in self.__players[1].pieces.items():
                if (
                    piece_v.get_owner() == cpu_piece.get_owner()
                    and piece_v.get_type() == cpu_piece.get_type()
                    and piece_v.get_position() == cpu_piece.get_position()
                ):
                    piece_key = piece_k
                    break

        if piece_key == "":
            raise ValueError("piece_keyが空です")

        target: Optional[Piece] = destination.get_piece()
        if target is not None and target.get_owner() != cpu_piece.get_owner():
            self.pick(destination, target)

        self.move(cpu_piece, piece_key, destination)

    # どのコマを選ぶか決定するアルゴリズム
    # cpuはプレイヤーの青のコマを取ることを優先する
    def _search_oppenent_blue_piece(self) -> Tuple[str, Piece, Block, bool]:
        cpu_piece: Optional[Piece] = None
        cpu_piece_key: str = ""
        destination: Optional[Block] = None
        does_capture: bool = False
        for piece_key, piece_value in self.__players[1].pieces.items():
            current_position: Optional[list[int]] = piece_value.get_position()
            if current_position is None:
                raise ValueError("選択したコマはすでにとられています")
            destination_position_list: list[list[int]] = [
                [current_position[0] + 1, current_position[1]],
                [current_position[0] - 1, current_position[1]],
                [current_position[0], current_position[1] + 1],
                [current_position[0], current_position[1] - 1],
            ]
            for destination_position in destination_position_list:
                if destination_position[0] not in range(0, 8) or destination_position[
                    1
                ] not in range(0, 8):
                    continue
                target: Optional[Piece] = self.__table[destination_position[0]][
                    destination_position[1]
                ].get_piece()
                if target is None:
                    continue
                if (
                    target.get_type() == "blue"
                    and target.get_owner() == self.__players[0].get_name()
                ):
                    cpu_piece_key = piece_key
                    cpu_piece = piece_value
                    destination = self.__table[destination_position[0]][
                        destination_position[1]
                    ]
                    does_capture = True
                    break
        # 射程内に青のコマがなかったらランダムに選択
        if cpu_piece is None:
            cpu_piece = random.choice(list(self.__players[1].pieces.values()))
        if destination is None:
            destination_x: int = random.randint(0, 7)
            destination_y: int = random.randint(0, 7)
            destination = self.__table[destination_y][destination_x]
        return (cpu_piece_key, cpu_piece, destination, does_capture)

    # CPUが選択したコマが移動可能かどうかを判定するメソッド（プレイヤーの移動チェックはフロントエンドで行う）
    def is_movable(self, piece: Piece, destination: Block) -> bool:
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
            return False
        return True

    def _is_escapable(self, turn: int) -> bool:
        for position in self.__escapable_positions[turn]:
            piece: Optional[Piece] = self.__table[position[0]][position[1]].get_piece()
            if piece is None:
                continue
            if (
                piece is not None
                and piece.get_owner() == self.__players[turn].get_name()
                and piece.get_type() == "blue"
            ):
                return True
        return False
