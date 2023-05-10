import pytest
from .geister import Piece, Block, Table


def test_is_movable():
    piece1 = Piece("test1", "blue")
    piece1.set_position([0, 0])
    # todo 青いオバケが脱出する場合は同じ位置を指定することで脱出可能
    # 同じ位置には移動できない
    # assert not Table._is_movable(piece1, Block([0, 0]))
    # 隣接しない位置には移動できない
    assert not Table._is_movable(piece1, Block([2, 0]))
    assert not Table._is_movable(piece1, Block([0, 2]))
    # 斜めには移動できない
    assert not Table._is_movable(piece1, Block([1, 1]))
    # ボードに存在しない位置には移動できない
    with pytest.raises(ValueError):
        Table._is_movable(piece1, Block([0, -1]))
        Table._is_movable(piece1, Block([-1, 0]))
    # 縦横1マスの位置には移動できる
    assert Table._is_movable(piece1, Block([0, 1]))
    assert Table._is_movable(piece1, Block([1, 0]))
    piece2 = Piece("test1", "red")
    piece2.set_position([7, 1])
    with pytest.raises(ValueError):
        Table._is_movable(piece2, Block([8, 1]))
    piece3 = Piece("test1", "blue")
    # 移動先に自分のコマがある場合は移動できない
    piece3.set_position([6, 1])
    block = Block([7, 1])
    block.set_piece(piece2)
    assert not Table._is_movable(piece3, block)
