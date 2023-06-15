from typing import Optional
from rest_framework import serializers
from .geister import Player, Table, Piece, Block


class PieceSerializer(serializers.Serializer):
    owner = serializers.CharField()
    type = serializers.CharField()
    position = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=7)
    )

    def create(self, validated_data) -> Piece:
        return Piece(**validated_data)

    def update(self, instance, validated_data):
        print("update PieceSerializer")
        instance.position = validated_data.get("position", instance.position)
        return instance

    def get_owner(self, obj: Piece) -> str:
        return obj.get_owner()

    def get_type(self, obj: Piece) -> str:
        return obj.get_type()

    def get_position(self, obj: Piece) -> Optional[list[int]]:
        return obj.get_position()


class BlockSerializer(serializers.Serializer):
    address = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=7)
    )
    piece = PieceSerializer(allow_null=True)

    def create(self, validated_data) -> Block:
        validated_data.pop("piece", None)
        return Block(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get("address", instance.address)
        instance.piece = validated_data.get("piece", instance.piece)
        return instance


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()
    pieces = serializers.SerializerMethodField()
    picked_blue_pieces_count = serializers.IntegerField(min_value=0, max_value=4, required=False)
    picked_red_pieces_count = serializers.IntegerField(min_value=0, max_value=4, required=False)

    def get_pieces(self, obj: Player) -> list[dict]:
        return [
            {
                "owner": piece.get_owner(),
                "type": piece.get_type(),
                "position": piece.get_position(),
            }
            for piece in obj.pieces.values()
        ]

    def get_picked_blue_pieces_count(self, obj: Player) -> int:
        return obj.get_picked_blue_pieces_count()

    def get_picked_red_pieces_count(self, obj: Player) -> int:
        return obj.get_picked_red_pieces_count()

    def create(self, validated_data) -> Player:
        validated_data.pop("picked_blue_pieces_count", 0)
        validated_data.pop("picked_red_pieces_count", 0)
        return Player(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.pieces = validated_data.get("pieces", instance.pieces)
        instance.picked_blue_pieces_count = validated_data.get(
            "picked_blue_pieces_count", instance.picked_blue_pieces_count
        )
        instance.picked_red_pieces_count = validated_data.get(
            "picked_red_pieces_count", instance.picked_red_pieces_count
        )
        return instance


class TableSerializer(serializers.Serializer):
    players = serializers.ListField(child=PlayerSerializer())
    winner = serializers.CharField(allow_blank=True)
    table = serializers.ListField(child=serializers.ListField(child=BlockSerializer()))
    turn = serializers.IntegerField(min_value=0, max_value=1)

    def get_turn(self, obj: Table) -> int:
        return obj.get_turn()

    def create(self, validated_data) -> Table:
        players_data = validated_data.pop("players", [])
        players = []
        for player_data in players_data:
            player_serializer = PlayerSerializer(data=player_data)
            if player_serializer.is_valid():
                players.append(player_serializer.save())
        validated_data.pop("winner", None)
        validated_data.pop("table", None)
        validated_data.pop("turn", None)
        return Table(players=players, **validated_data)

    def update(self, instance, validated_data):
        current_table_data = validated_data.pop("table", None)
        if current_table_data is not None:
            for i, row_data in enumerate(current_table_data):
                for j, block_data in enumerate(row_data):
                    block_serializer = BlockSerializer(
                        instance=instance.table[i][j], data=block_data
                    )
                    if block_serializer.is_valid():
                        instance[i][j] = block_serializer.save()
        return instance
