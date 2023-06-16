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
        piece = validated_data.pop("piece", None)
        return Block(**validated_data, piece=piece)

    def update(self, instance, validated_data):
        instance.address = validated_data.get("address", instance.address)
        instance.piece = validated_data.get("piece", instance.piece)
        return instance


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()
    pieces = serializers.DictField(child=PieceSerializer(), required=False)
    picked_blue_pieces_count = serializers.IntegerField(
        min_value=0, max_value=4, required=False
    )
    picked_red_pieces_count = serializers.IntegerField(
        min_value=0, max_value=4, required=False
    )

    def create(self, validated_data) -> Player:
        pieces = validated_data.pop("pieces", None)
        validated_data.pop("picked_blue_pieces_count", 0)
        validated_data.pop("picked_red_pieces_count", 0)
        return Player(pieces=pieces, **validated_data)

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
    winner = serializers.CharField(allow_blank=True, required=False)
    table = serializers.ListField(
        child=serializers.ListField(child=BlockSerializer()), required=False
    )
    turn = serializers.IntegerField(min_value=0, max_value=1, required=False)

    def get_players(self, obj: Table) -> list[Player]:
        return obj.get_players()

    def get_winner(self, obj: Table) -> str:
        return obj.get_winner()

    def get_table(self, obj: Table) -> list[list[Block]]:
        return obj.get_table()

    def get_turn(self, obj: Table) -> int:
        return obj.get_turn()

    def create(self, validated_data) -> Table:
        players_data = validated_data.pop("players", [])
        players = []
        for player_data in players_data:
            # ここでplayer_dataの中身（piecesのposition）を確認してみる
            # NoneになっていなければOK
            # player_serializerの中身(piece_serializer)を確認してみる
            # NoneになっていなければOK
            player_serializer = PlayerSerializer(data=player_data)
            if player_serializer.is_valid():
                players.append(player_serializer.save())
        validated_data.pop("winner", "")
        # validated_dataのtableの中身を確認してみる
        # Blockのpieceが全てのマスでNoneになっているか確認してみる
        # NoneになっていなければOK（配置されているマスはNoneではないはず）
        table_data = validated_data.pop("table", None)
        table = []
        for row_data in table_data:
            row = []
            for block_data in row_data:
                block_serializer = BlockSerializer(data=block_data)
                if block_serializer.is_valid():
                    row.append(block_serializer.save())
            table.append(row)
        validated_data.pop("turn", None)
        return Table(players=players, table=table, **validated_data)

    def to_representation(self, instance: Table):
        rep = super().to_representation(instance)
        rep["players"] = PlayerSerializer(instance.players, many=True).data
        rep["table"] = [
            [BlockSerializer(block).data for block in row] for row in instance.table
        ]
        return rep

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
