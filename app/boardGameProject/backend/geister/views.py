from typing import Optional, Tuple
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from .geister import Table, Player, Piece, Block
from .serializers import (
    PlayerSerializer,
    TableSerializer,
    PieceSerializer,
    BlockSerializer,
)

import json


@api_view(["POST"])
def start_game(request: Request) -> Response:
    player_data = request.data
    print(player_data)
    player_serializer = PlayerSerializer(data=player_data, many=True)
    if player_serializer.is_valid():
        players = player_serializer.save()
        table = Table(players)
        table_serializer = TableSerializer(table)
        serialized_data = table_serializer.data
        request.session["table"] = serialized_data
        json_data = json.dumps(serialized_data)
        print(json_data)
        return Response(serialized_data, status=status.HTTP_201_CREATED)
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
        updated_table_serializer = TableSerializer(updated_table)
        request.session["table"] = TableSerializer(updated_table).data
        return Response(updated_table_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(table_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_table_serializer(
    data: dict,
) -> Tuple[Optional[Table], Optional[Response]]:
    table_serializer = TableSerializer(data=data)
    if table_serializer.is_valid():
        return table_serializer.create(table_serializer.validated_data), None
    else:
        return None, Response(
            table_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


def get_players_serializer(
    data: list[dict],
) -> Tuple[Optional[list[Player]], Optional[Response]]:
    player_serializer = PlayerSerializer(data=data, many=True)
    if player_serializer.is_valid():
        players_data = player_serializer.validated_data
        players = []
        for player_data in players_data:
            pieces = {k: Piece(**v) for k, v in player_data["pieces"].items()}
            player = Player(name=player_data["name"], pieces=pieces)
            players.append(player)
        return players, None
    else:
        return None, Response(
            player_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


def get_piece_serializer(
    data: dict,
) -> Tuple[Optional[Piece], Optional[Response]]:
    piece_serializer = PieceSerializer(data=data)
    if piece_serializer.is_valid():
        piece_data = piece_serializer.validated_data
        piece = Piece(**piece_data)
        return piece, None
    else:
        return None, Response(
            piece_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


def get_block_serializer(
    data: dict,
) -> Tuple[Optional[Block], Optional[Response]]:
    block_serializer = BlockSerializer(data=data)
    if block_serializer.is_valid():
        return block_serializer.save(), None
    else:
        return None, Response(
            block_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


def get_piece_key_from_players(
    players_data: list[dict], piece_key: str
) -> Tuple[Optional[dict], Optional[Response]]:
    for player in players_data:
        if piece_key in player["pieces"]:
            return player["pieces"][piece_key], None
    return None, Response(
        {"error": "piece_key not found"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
def move_piece(request: Request) -> Response:
    session_table = request.session.get("table")
    if session_table is None:
        return Response(
            {"detail": "Session data not found"}, status=status.HTTP_400_BAD_REQUEST
        )
    table, error_response = get_table_serializer(session_table)
    if error_response:
        return error_response
    if table is None:
        return Response(
            {"detail": "Session data not found"}, status=status.HTTP_400_BAD_REQUEST
        )

    players, error_response = get_players_serializer(request.data["players"])
    if error_response:
        return error_response
    if players is None:
        return Response(
            {"detail": "request.data['players'] is None"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    piece_key = request.data["piece_key"]

    player_piece, error_response = get_piece_serializer(request.data["player_piece"])
    if error_response:
        return error_response
    if player_piece is None:
        return Response(
            {"detail": "request.data['player_piece'] is None"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    destination, error_response = get_block_serializer(request.data["destination"])

    if error_response:
        return error_response
    if destination is None:
        return Response(
            {"detail": "request.data['destination'] is None"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    current_turn: int = session_table["turn"]
    print(players, type(players))
    print(player_piece, type(player_piece))
    print(piece_key, type(piece_key))
    print(destination, type(destination))
    table.move(players[current_turn], player_piece, piece_key, destination)
    table.switch_turn()

    updated_table = TableSerializer(table).data
    request.session["table"] = updated_table
    return Response(updated_table, status=status.HTTP_200_OK)
