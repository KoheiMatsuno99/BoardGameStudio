from rest_framework import serializers
from .geister import Table, Player


class TableSerializer(serializers.Serializer):
    players = serializers.StringRelatedField(many=True)
    winner = serializers.CharField()

    def create(self, validated_data) -> Table:
        return Table(**validated_data)

    def update(self, instance, validated_data):
        pass


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()
    pieces = serializers.StringRelatedField(many=True)

    def create(self, validated_data) -> Player:
        return Player(**validated_data)

    def update(self, instance, validated_data):
        pass
