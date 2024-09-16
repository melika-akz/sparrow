from rest_framework import serializers

from authorize.models import User
from ..models import Room


class RoomSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Room
        fields = ['member_id']

    def validate(self, data):
        member_id = data.get('member_id')
        if member_id == self.context['request'].user.id:
            raise serializers.ValidationError('You cannot create a room to chat with yourself.')
        return data

    def create(self, validated_data):
        member_id = validated_data.pop('member_id')
        room = super().create(validated_data)
        # Add members
        room.add_member(self.context['request'].user)
        room.add_member(User.objects.get(id=member_id))
        return room

