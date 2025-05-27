from rest_framework import serializers
from django.core.exceptions import ValidationError

from authorize.models import Member
from authorize.serializers import MemberSerializer
from ..models import Room
from ..entities import RoomRepository
from ..constants import DIRECT, CHANNEL, GROUP


class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    members = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Room
        fields = ['id', 'members', 'type', 'name']

    def validate(self, data):
        """Prevent users from creating a direct chat with themselves."""
        members = data.get('members', [])
        print(members)
        if members is None:
            raise ValidationError('Room must have at least one member.')

        if data.get('type') not in [CHANNEL, GROUP]:
            raise ValidationError('Invalid room type. Allowed: Channel, Group.')

        return data

    def create(self, validated_data):
        """Create a room based on type."""
        current_member = self.context['request'].user
        return self._create_room(validated_data, current_member)

    def _create_direct(self, validated_data, current_member):
        """Create or retrieve an existing direct room."""
        destination_member_id = validated_data.pop('member_id')
        destination_member = Member.objects.filter(id=destination_member_id).first()

        if not destination_member:
            raise ValidationError('Member does not exist.')

        room = RoomRepository.check_exist_direct_room(
            destination_id=destination_member.id,
            source_id=current_member.id
        )

        if room is None:
            room = self._initialize_room(
                name=destination_member.full_name(),
                type=DIRECT,
                members=[current_member, destination_member]
            )
        return room

    def _create_room(self, validated_data, current_member):
        """Create a new group room or retrieve an existing one."""
        room = RoomRepository.check_exist_room(
            name=validated_data['name'],
            type_=validated_data['type']
        )

        if room is None:
            room = self._initialize_room(
                name=validated_data['name'],
                type=validated_data['type'],
                members=[current_member.id] + validated_data['members']
            )

        return room

    def _initialize_room(self, name, type, members):
        """Helper function to create a room and add members."""
        room = Room.objects.create(name=name, type=type)
        for member_id in members:
            member = Member.objects.get(id=member_id)
            room.add_member(member, room)
        return room


class RoomDetailSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'type', 'members']