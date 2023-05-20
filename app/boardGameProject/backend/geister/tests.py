from .geister import Piece, Table, Player


def test_is_movable():
    t = Table([Player("test1"), Player("test2")])
    table = t.get_table()
    piece1 = Piece("test1", "blue")
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
    piece2 = Piece("test1", "red")
    piece2.set_position([7, 1])
    # 同じ場所には移動できない
    assert not t._is_movable(piece2, table[7][1])
    piece3 = Piece("test1", "blue")
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
