import pytest
from .geister import Piece, Table, Player


def test_is_movable():
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    piece1 = Piece(t.get_players()[0], "blue")
    piece1.set_position([0, 0])
    table[0][0].set_piece(piece1)
    # todo 青いオバケが脱出する場合は同じ位置を指定することで脱出可能
    # assert t._is_movable(piece1, Block([0, 0]))
    # 隣接しない位置には移動できない
    assert not t._is_movable(piece1, table[2][0])
    assert not t._is_movable(piece1, table[0][2])
    # 斜めには移動できない
    assert not t._is_movable(piece1, table[1][1])
    # 縦横1マスの位置には移動できる
    assert t._is_movable(piece1, table[0][1])
    assert t._is_movable(piece1, table[1][0])
    piece2 = Piece(t.get_players()[0], "red")
    piece2.set_position([7, 1])
    # 同じ場所には移動できない
    assert not t._is_movable(piece2, table[7][1])
    piece3 = Piece(t.get_players()[0], "blue")
    # 移動先に自分のコマがある場合は移動できない
    piece3.set_position([6, 1])
    block2 = table[7][1]
    block2.set_piece(piece2)
    assert not t._is_movable(piece3, table[7][1])


def test_is_escapable():
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    assert not t._is_escapable(t.get_players()[0])
    table[0][7].set_piece(Piece(t.get_players()[0], "red"))
    assert not t._is_escapable(t.get_players()[0])
    table[7][0].set_piece(Piece(t.get_players()[0], "blue"))
    assert not t._is_escapable(t.get_players()[0])
    table[0][0].set_piece(Piece(t.get_players()[0], "blue"))
    assert t._is_escapable(t.get_players()[0])
    assert not t._is_escapable(t.get_players()[1])


def test_pick_with_empty_destination():
    table = Table([Player("test1"), Player("test2")])
    player = table.get_players()[0]
    empty_block = table.get_table()[0][0]

    with pytest.raises(ValueError):
        table._pick(player, empty_block)


def test_pick_with_opponent_piece_not_last():
    table = Table([Player("test1"), Player("test2")])
    player1, player2 = table.get_players()
    destination_block = table.get_table()[0][0]
    piece = Piece(player2.get_name(), "blue")
    destination_block.set_piece(piece)
    player2.pieces["piece1"] = piece

    table._pick(player1, destination_block)

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

    table._pick(player1, block1)
    table._pick(player1, block2)
    table._pick(player1, block3)
    table._pick(player1, block4)

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

    table._pick(player1, block1)
    table._pick(player1, block2)
    table._pick(player1, block3)
    table._pick(player1, block4)

    assert piece1 not in player2.pieces.values()
    assert player1.get_picked_red_pieces_count() == 4
    assert table.get_winner() == player2.get_name()


def test_move():
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    piece1 = Piece(t.get_players()[0], "blue")
    piece1.set_position([0, 0])
    table[0][0].set_piece(piece1)
    with pytest.raises(ValueError):
        t.move(t.get_players()[0], None, table[0][1])
    with pytest.raises(ValueError):
        t.move(t.get_players()[0], piece1, None)
    t.move(t.get_players()[0], piece1, table[0][1])
    assert t.get_winner() == t.get_players()[0].get_name()

    piece2 = Piece(t.get_players()[1], "blue")
    piece2.set_position([5, 1])
    table[5][1].set_piece(piece2)
    t.move(t.get_players()[1], piece2, table[5][2])
    assert table[5][1].get_piece() is None
    assert piece2.get_position() == [5, 2]
    assert table[5][2].get_piece() == piece2

    piece3 = Piece(t.get_players()[1], "red")
    piece3.set_position([2, 5])
    table[2][5].set_piece(piece3)
    piece4 = Piece(t.get_players()[0], "red")
    piece4.set_position([3, 5])
    table[3][5].set_piece(piece4)
    t.move(t.get_players()[1], piece3, table[3][5])
    assert piece4 not in t.get_players()[0].pieces.values()
    assert table[2][5].get_piece() is None
    assert piece3.get_position() == [3, 5]

    piece5 = Piece(t.get_players()[1], "red")
    piece5.set_position(None)
    with pytest.raises(ValueError):
        t.move(t.get_players()[1], piece5, table[3][1])
