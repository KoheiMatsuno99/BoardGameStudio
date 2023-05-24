# Create your views here.
from typing import Optional

from rest_framework import api_view, status
from rest_framework.response import Response
from rest_framework.request import Request

from .geister import Block, Piece, Player, Table
from .serializers import PlayerSerializer, TableSerializer


@api_view(["POST"])
def start_game(request: Request) -> Response:
    player_data = request.data
    player_serializer = PlayerSerializer(data=player_data, many=True)
    if player_serializer.is_valid():
        players = player_serializer.save()
        table = Table(players)
        request.session["table"] = table
        table_serializer = TableSerializer(table)
        return Response(table_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(player_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def move_piece(request) -> Response:
    table: Table = request.session.get("table")
    if table is None:
        return Response({"error": "ゲームが開始されていません"}, status=status.HTTP_400_BAD_REQUEST)
    player: Player = request.data["player"]
    player_piece: Optional[Piece] = request.data["player_piece"]
    destination: Block = request.data["destination"]
    table.move(player, player_piece, destination)
    table_selializer = TableSerializer(table)
    return Response(table_selializer.data, status=status.HTTP_200_OK)
