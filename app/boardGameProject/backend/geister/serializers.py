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
    piece = PieceSerializer()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()
    pieces = serializers.SerializerMethodField()

    def get_pieces(self, obj: Player) -> list[dict]:
        return [
            {
                "owner": piece.get_owner(),
                "type": piece.get_type(),
                "position": piece.get_position(),
            }
            for piece in obj.pieces.values()
        ]

    def create(self, validated_data) -> Player:
        return Player(**validated_data)

    def update(self, instance, validated_data):
        pass


class TableSerializer(serializers.Serializer):
    players = serializers.ListField(child=PlayerSerializer())
    winner = serializers.CharField()
    table = serializers.ListField(child=serializers.ListField(child=BlockSerializer()))

    # def get_players(self, obj: Table) -> list[str]:
    #     return [player.get_name() for player in obj.get_players()]

    def create(self, validated_data) -> Table:
        return Table(**validated_data)

    def update(self, instance, validated_data):
        pass
