from .geister import Piece, Table, Player


"""
Tableクラスのis_movable()のテスト
"""

# フロントエンドで移動のバリデーションを行うため、一旦コメントアウト
# def test_not_movable_separate_block():
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([3, 3])
#     table[3][3].set_piece(piece1)
#     # 隣接しない位置には移動できない
#     assert not t._is_movable(piece1, table[3][5])
#     assert not t._is_movable(piece1, table[3][1])
#     assert not t._is_movable(piece1, table[1][3])
#     assert not t._is_movable(piece1, table[5][3])

#     piece2 = Piece(t.get_players()[0].get_name(), "blue")
#     piece2.set_position([0, 0])
#     table[0][0].set_piece(piece2)
#     # 隣接しない位置には移動できない
#     assert not t.is_movable(piece2, table[2][0])
#     assert not t.is_movable(piece2, table[0][2])


# def test_not_movable_cross_block():
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([4, 6])
#     table[4][6].set_piece(piece1)
#     # 斜めには移動できない
#     assert not t._is_movable(piece1, table[3][5])
#     assert not t._is_movable(piece1, table[5][7])
#     assert not t._is_movable(piece1, table[5][5])
#     assert not t._is_movable(piece1, table[3][7])

#     piece2 = Piece(t.get_players()[0].get_name(), "blue")
#     piece2.set_position([0, 0])
#     table[0][0].set_piece(piece2)
#     # 斜めには移動できない
#     assert not t._is_movable(piece2, table[1][1])


# def test_not_movable_same_block():
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([4, 6])
#     table[4][6].set_piece(piece1)
#     # 同じ場所には移動できない
#     assert not t._is_movable(piece1, table[4][6])

#     piece2 = Piece(t.get_players()[0].get_name(), "blue")
#     piece2.set_position([0, 0])
#     table[0][0].set_piece(piece2)
#     # 同じ場所には移動できない
#     assert not t._is_movable(piece2, table[0][0])


# def test_not_movable_block_with_my_piece():
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([4, 6])
#     table[4][6].set_piece(piece1)
#     piece2 = Piece(t.get_players()[0].get_name(), "blue")
#     piece2.set_position([4, 5])
#     table[4][5].set_piece(piece2)
#     # 移動先に自分のコマがある場合は移動できない
#     assert not t._is_movable(piece1, table[4][5])


# def test_is_moveable_block_with_opponent_piece():
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([4, 6])
#     table[4][6].set_piece(piece1)
#     piece2 = Piece(t.get_players()[1].get_name(), "blue")
#     piece2.set_position([4, 5])
#     table[4][5].set_piece(piece2)
#     # 移動先に相手のコマがある場合は移動できる
#     assert t._is_movable(piece1, table[4][5])

#     piece3 = Piece(t.get_players()[0].get_name(), "red")
#     piece3.set_position([0, 0])
#     table[0][0].set_piece(piece3)
#     piece4 = Piece(t.get_players()[1].get_name(), "blue")
#     piece4.set_position([0, 1])
#     table[0][1].set_piece(piece4)
#     # 移動先に相手のコマがある場合は移動できる
#     assert t._is_movable(piece3, table[0][1])


# def test_is_movable():
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([0, 0])
#     table[0][0].set_piece(piece1)
#     # 隣接する位置かつ目的地にコマがない場合は移動できる
#     assert t._is_movable(piece1, table[0][1])
#     assert t._is_movable(piece1, table[1][0])


"""
Table._is_escapable()のテスト
"""


def test_not_escapable_block_of_oppenent_on_my_piece():
    """
    プレイヤー0の脱出マスは[0, 0], [0, 7]
    プレイヤー1の脱出マスは[7, 0], [7, 7]
    """
    # 自分の脱出マスに自分のコマがない
    # かつ、相手の脱出マスに自分のコマがある場合は脱出できない
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    piece1 = Piece(t.get_players()[0].get_name(), "blue")
    piece1.set_position([7, 0])
    table[7][0].set_piece(piece1)
    assert not t._is_escapable(0)

    piece2 = Piece(t.get_players()[1].get_name(), "blue")
    piece2.set_position([0, 0])
    table[0][0].set_piece(piece2)
    assert not t._is_escapable(1)


def test_not_escapable_block_of_mine_on_my_red_piece():
    """
    プレイヤー0の脱出マスは[0, 0], [0, 7]
    プレイヤー1の脱出マスは[7, 0], [7, 7]
    """
    # 自分の脱出マスにコマがあっても赤いコマであれば脱出できない
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    piece1 = Piece(t.get_players()[0].get_name(), "red")
    piece1.set_position([0, 0])
    table[0][0].set_piece(piece1)
    assert not t._is_escapable(0)

    piece2 = Piece(t.get_players()[0].get_name(), "red")
    piece2.set_position([0, 7])
    table[0][7].set_piece(piece2)
    assert not t._is_escapable(0)

    piece3 = Piece(t.get_players()[1].get_name(), "red")
    piece3.set_position([7, 0])
    table[7][0].set_piece(piece3)
    assert not t._is_escapable(1)

    piece4 = Piece(t.get_players()[1].get_name(), "red")
    piece4.set_position([7, 7])
    table[7][7].set_piece(piece4)
    assert not t._is_escapable(1)


def test_is_escapable_block_of_mine_on_my_blue_piece():
    """
    プレイヤー0の脱出マスは[0, 0], [0, 7]
    プレイヤー1の脱出マスは[7, 0], [7, 7]
    """
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    piece1 = Piece(t.get_players()[0].get_name(), "blue")
    piece1.set_position([0, 0])
    table[0][0].set_piece(piece1)
    # 自分の脱出マスに青いコマがあれば脱出可能
    assert t._is_escapable(0)
    # 脱出可能なコマがあれば他の脱出マスに赤いコマがあっても問題ない
    piece2 = Piece(t.get_players()[0].get_name(), "red")
    piece2.set_position([0, 7])
    table[0][7].set_piece(piece2)
    # piece2は脱出不可だが、piece1が脱出可能なのでTrue
    assert t._is_escapable(0)
    # プレイヤー0は脱出条件を満たしているが、プレイヤー1は満たしていないのでFalse
    assert not t._is_escapable(1)


"""
Tableクラスの_pick()のテスト
"""


def test_pick_with_opponent_piece_not_last():
    table = Table([Player("test1"), Player("test2")])
    player1, player2 = table.get_players()
    destination_block = table.get_table()[0][0]
    piece = Piece(player2.get_name(), "blue")
    destination_block.set_piece(piece)
    player2.pieces["piece1"] = piece

    table.pick(destination_block, piece)

    assert piece not in player2.pieces.values()
    assert player1.get_picked_blue_pieces_count() == 1
    assert table.get_winner() == ""


def test_pick_with_last_blue_piece():
    table = Table([Player("test1"), Player("test2")])
    player1, player2 = table.get_players()
    block1 = table.get_table()[0][0]
    piece1 = Piece(player2.get_name(), "blue")
    block1.set_piece(piece1)
    player2.pieces["piece1"] = piece1
    block2 = table.get_table()[3][6]
    piece2 = Piece(player2.get_name(), "blue")
    block2.set_piece(piece2)
    player2.pieces["piece2"] = piece2
    block3 = table.get_table()[2][2]
    piece3 = Piece(player2.get_name(), "blue")
    block3.set_piece(piece3)
    player2.pieces["piece3"] = piece3
    block4 = table.get_table()[2][5]
    piece4 = Piece(player2.get_name(), "blue")
    block4.set_piece(piece4)
    player2.pieces["piece4"] = piece4

    table.pick(block1, piece1)
    table.pick(block2, piece2)
    table.pick(block3, piece3)
    table.pick(block4, piece4)

    assert piece1 not in player2.pieces.values()
    assert piece2 not in player2.pieces.values()
    assert piece3 not in player2.pieces.values()
    assert piece4 not in player2.pieces.values()
    assert player1.get_picked_blue_pieces_count() == 4
    assert table.get_winner() == player1.get_name()


def test_pick_with_last_red_piece():
    table = Table([Player("test1"), Player("test2")])
    player1, player2 = table.get_players()
    block1 = table.get_table()[0][0]
    piece1 = Piece(player2.get_name(), "red")
    block1.set_piece(piece1)
    player2.pieces["piece1"] = piece1
    block2 = table.get_table()[3][6]
    piece2 = Piece(player2.get_name(), "red")
    block2.set_piece(piece2)
    player2.pieces["piece2"] = piece2
    block3 = table.get_table()[2][2]
    piece3 = Piece(player2.get_name(), "red")
    block3.set_piece(piece3)
    player2.pieces["piece3"] = piece3
    block4 = table.get_table()[2][5]
    piece4 = Piece(player2.get_name(), "red")
    block4.set_piece(piece4)
    player2.pieces["piece4"] = piece4

    table.pick(block1, piece1)
    table.pick(block2, piece2)
    table.pick(block3, piece3)
    table.pick(block4, piece4)

    assert piece1 not in player2.pieces.values()
    assert player1.get_picked_red_pieces_count() == 4
    assert table.get_winner() == player2.get_name()


"""
Tableクラスのmove()のテスト
"""


# def test_move_no_piece_on_destination():
#     # 移動先にコマがない場合の挙動をテスト
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([5, 3])
#     table[5][3].set_piece(piece1)
#     " [5, 3] -> [5, 4]に移動"
#     t.move(t.get_players()[0], piece1, table[5][4])
#     # [5, 3]にはもういないこと
#     assert table[5][3].get_piece() is None
#     # [5, 4]にいること
#     assert table[5][4].get_piece() == piece1
#     assert piece1.get_position() == [5, 4]


# def test_move_oppenent_piece_on_destination():
#     # 移動先に相手のコマがある場合の挙動をテスト
#     t = Table([Player("test1"), Player("test2")])
#     table = t.get_table()
#     piece1 = Piece(t.get_players()[0].get_name(), "blue")
#     piece1.set_position([5, 3])
#     table[5][3].set_piece(piece1)
#     piece2 = Piece(t.get_players()[1].get_name(), "red")
#     piece2.set_position([5, 4])
#     table[5][4].set_piece(piece2)
#     " [5, 3] -> [5, 4]に移動"
#     t.move(t.get_players()[0], piece1, table[5][4])
#     # [5, 3]にはもういないこと
#     assert table[5][3].get_piece() is None
#     # [5, 4]にいること
#     assert table[5][4].get_piece() == piece1
#     assert piece1.get_position() == [5, 4]
#     # 相手のコマが取られていること
#     assert piece2.get_position() is None
#     assert piece2 not in t.get_players()[1].pieces.values()
