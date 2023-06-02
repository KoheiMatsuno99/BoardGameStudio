from typing import Optional

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from .geister import Block, Piece, Player, Table
from .serializers import PlayerSerializer, TableSerializer


@api_view(["POST"])
def start_game(request: Request) -> Response:
    player_data = request.data
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
    print('new_request_data is following this')
    print("----------")
    print(f'{new_table_data}')
    print("----------")
    table_serializer = TableSerializer(data=current_table_data)
    if table_serializer.is_valid():
        updated_table = table_serializer.save()
        request.session["table"] = TableSerializer(updated_table).save()
        return Response(request.session["table"], status=status.HTTP_200_OK)
    else:
        return Response(table_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def move_piece(request: Request) -> Response:
    table = request.session.get("table")
    if table is None:
        return Response({"error": "ゲームが開始されていません"}, status=status.HTTP_400_BAD_REQUEST)
    player: Player = request.data["player"]
    player_piece: Optional[Piece] = request.data["player_piece"]
    destination: Block = request.data["destination"]
    table.move(player, player_piece, destination)
    table_selializer = TableSerializer(table)
    return Response(table_selializer.data, status=status.HTTP_200_OK)
