from rest_framework import serializers

from .geister import Player, Table


class PieceSerializer(serializers.Serializer):
    owner = serializers.CharField()
    type = serializers.CharField()
    position = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=7)
    )


class BlockSerializer(serializers.Serializer):
    address = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=7)
    )
    piece = PieceSerializer(allow_null=True)

    def update(self, instance, validated_data):
        instance.address = validated_data.get("address", instance.address)
        instance.piece = validated_data.get("piece", instance.piece)
        return instance


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()
    pieces = serializers.SerializerMethodField()
    picked_blue_pieces_count = serializers.IntegerField(min_value=0, max_value=4)
    picked_red_pieces_count = serializers.IntegerField(min_value=0, max_value=4)

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
        validated_data.pop("picked_blue_pieces_count", None)
        validated_data.pop("picked_red_pieces_count", None)
        return Player(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.pieces = validated_data.get("pieces", instance.pieces)
        return instance


class TableSerializer(serializers.Serializer):
    players = serializers.ListField(child=PlayerSerializer())
    winner = serializers.CharField(allow_blank=True)
    table = serializers.ListField(child=serializers.ListField(child=BlockSerializer()))
    
    def create(self, validated_data) -> Table:
        validated_data.pop("winner", None)
        validated_data.pop("table", None)
        return Table(**validated_data)

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
