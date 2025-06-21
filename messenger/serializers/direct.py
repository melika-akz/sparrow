from django.shortcuts import get_object_or_404
from rest_framework import serializers

from authorize.models import Member
from .message import MessageSerializer
from .room_member import RoomMemberSerializer
from ..constants import DIRECT
from ..entities import RoomRepository
from ..models import Room


class DirectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    member_id = serializers.IntegerField(write_only=True, required=False)
    members = RoomMemberSerializer(source='room_members', many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'members', 'member_id', 'type', 'name', 'messages']

    def validate(self, data):
        member_id = data.get('member_id')
        current_member = self.context['request'].user

        if member_id == current_member.id:
            raise serializers.ValidationError('You cannot create a direct with yourself.')

        if not Member.objects.filter(id=member_id).exists():
            raise serializers.ValidationError({'member_id': 'The selected member does not exist.'})

        return data

    def create(self, validated_data):
        current_member = self.context['request'].user
        type_ = validated_data['type']

        if type_ != DIRECT:
            raise serializers.ValidationError({'type': 'Invalid direct chat type.'})

        return self.create_direct(validated_data, current_member)

    @staticmethod
    def create_direct(validated_data, current_member):
        """Handles the creation of direct messages between two members."""
        destination_member_id = validated_data.pop('member_id')
        destination_member = get_object_or_404(Member, id=destination_member_id)

        room, created = RoomRepository.get_or_create_direct_room(
            destination_member=destination_member,
            current_member=current_member
        )

        if created:
            room.name = destination_member.full_name()
            room.save()
            room.add_member(current_member)
            room.add_member(destination_member)
        return room


