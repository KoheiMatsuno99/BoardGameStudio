from rest_framework import serializers

from .geister import Player, Table


class BlockSerializer(serializers.Serializer):
    position = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=7)
    )
    piece = serializers.StringRelatedField(allow_null=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TableSerializer(serializers.Serializer):
    players = serializers.StringRelatedField(many=True)
    winner = serializers.CharField()
    table = serializers.ListField(child=BlockSerializer(many=True))

    def create(self, validated_data) -> Table:
        return Table(**validated_data)

    def update(self, instance, validated_data):
        pass


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data) -> Player:
        return Player(**validated_data)

    def update(self, instance, validated_data):
        pass
