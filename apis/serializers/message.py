from rest_framework import serializers, exceptions

from authorize.serializers import MemberSerializer
from ..models import Message, RoomMember


class MessageSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'body', 'sender_id', 'created_at', 'seen_at', 'seen_by', 'room_id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sender'] = MemberSerializer(instance.sender).data
        return data

    def validate(self, data):
        sender = self.context['request'].user
        room = self.context['room']

        if not RoomMember.objects.filter(member_id=sender.id, room_id=room.id).exists():
            raise exceptions.ValidationError('You cannot send a message in a room that you are not a member of')

        return data

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        validated_data['room'] = self.context['room']
        return super().create(validated_data)

