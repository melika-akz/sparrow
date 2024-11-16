from rest_framework import serializers, exceptions

from ..entities import RoomRepository
from ..models import Message, RoomMember


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'body', 'sender_id', 'created_at', 'seen_at', 'room_id']

    def validate(self, data):
        sender = self.context['request'].user
        room = self.context['room']
        data['room'] = room
        data['sender'] = sender

        if not RoomMember.objects.filter(member_id=sender.id, room_id=room.id).exists():
            raise exceptions.ValidationError('You cannot send a message in a room that you are not a member of')
        return data

