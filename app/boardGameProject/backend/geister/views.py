from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from .geister import Block, Piece, Player, Table
from .serializers import (
    PlayerSerializer,
    TableSerializer,
    PieceSerializer,
    BlockSerializer,
)


@api_view(["POST"])
def start_game(request: Request) -> Response:
    player_data = request.data
    print(player_data)
    player_serializer = PlayerSerializer(data=player_data, many=True)
    if player_serializer.is_valid():
        players: list[Player] = player_serializer.save()
        table = Table(players)
        serialized_table = TableSerializer(table)
        request.session["table"] = serialized_table.data
        table_serializer = TableSerializer(table)
        print(table_serializer.data)
        return Response(table_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_ready(request: Request) -> Response:
    print("Received data of initial positions")
    print(f"Session ID get_ready: {request.session.session_key}")
    current_table_data = request.session.get("table")
    if current_table_data is None:
        return Response(
            {"detail": "Session data not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    new_table_data = request.data
    if isinstance(new_table_data, list):
        new_table_data = {
            "players": current_table_data.get("players"),
            "winner": current_table_data.get("winner", ""),
            "table": new_table_data,
            "turn": current_table_data.get("turn"),
        }
    print("----------")
    print("----------")
    print("new data is following this;")
    print("----------")
    print(new_table_data)
    print("----------")
    print("----------")
    table_serializer = TableSerializer(data=new_table_data)
    if table_serializer.is_valid():
        updated_table = table_serializer.save()
        request.session["table"] = TableSerializer(updated_table).data
        return Response(request.session["table"], status=status.HTTP_200_OK)
    else:
        return Response(table_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def move_piece(request: Request) -> Response:
    table_data = request.session.get("table")
    if table_data is None:
        return Response({"error": "ゲームが開始されていません"}, status=status.HTTP_400_BAD_REQUEST)
    print("table_data", table_data)
    table_selializer = TableSerializer(data=table_data)
    # todo Serializerに渡すデータをlist -> dictにする
    players_data = request.data["players"]
    if isinstance(players_data, list):
        players_data = {"player0": players_data[0], "player1": players_data[1]}
    print("type of players_data", type(players_data))
    print(players_data)
    players_serializer = PlayerSerializer(data=players_data)

    player_piece_data = request.data["player_piece"]
    player_piece_serializer = PieceSerializer(data=player_piece_data)
    destination_data = request.data["destination"]
    destination_serializer = BlockSerializer(data=destination_data)
    if (
        table_selializer.is_valid()
        and players_serializer.is_valid()
        and player_piece_serializer.is_valid()
        and destination_serializer.is_valid()
    ):
        table: Table = table_selializer.save()
        players: list[Player] = players_serializer.save()
        print(players, type(players))
        player_piece: Piece = player_piece_serializer.save()
        print(player_piece, type(player_piece))
        destination: Block = destination_serializer.save()
        print(destination, type(destination))
        # players[0]は仮置き
        # Tableクラスにターンを新たなフィールドとして作成
        current_turn = request.session.get("turn")
        print("current_turn", current_turn)
        table.move(players[0], player_piece, destination)
        # todo
        # 更新したtableをtable_serializerに渡す
        # 更新したtableをsessionに保存
        return Response(table_selializer.data, status=status.HTTP_200_OK)
    elif not table_selializer.is_valid():
        return Response(
            {"table_serializer": table_selializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif not players_serializer.is_valid():
        return Response(
            {"players_serializer": players_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif not player_piece_serializer.is_valid():
        return Response(
            {"player_piece_serializer": player_piece_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return Response(
            {"destination_serializer": destination_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
