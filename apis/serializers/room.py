from rest_framework import serializers

from authorize.models import Member

from ..entities import RoomRepository
from ..models import Room
from .room_member import RoomMemberSerializer


class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    member_id = serializers.IntegerField(write_only=True, required=False)
    members = RoomMemberSerializer(source='room_members', many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'members', 'member_id', 'type', 'name']

    def validate(self, data):
        member_id = data.get('member_id')
        if member_id == self.context['request'].user.id:
            raise serializers.ValidationError('You cannot create a room to chat with yourself.')
        return data

    def create(self, validated_data):
        current_member = self.context['request'].user
        type_ = validated_data['type']
        if type_ == 'D' or type_ == 'Direct':
            room = self.create_direct(
                current_member=current_member,
                validated_data=validated_data
            )
        else:
            room = self.create_room(
                current_member=current_member,
                validated_data=validated_data
            )
        return room

    @staticmethod
    def create_direct(validated_data, current_member):
        destination_member_id = validated_data.pop('member_id')
        destination_member = Member.objects.filter(id=destination_member_id).first()
        if destination_member is None:
            raise serializers.ValidationError('Member Not Exist')

        room = RoomRepository.check_exist_direct_room(
            destination_id=destination_member.id,
            source_id=current_member.id
        )
        if room is None:
            room = Room.objects.create(
                name=f'{destination_member.full_name()}',
                type='D'
            )
            room.add_member(current_member, room)
            room.add_member(destination_member, room)
        return room

    @staticmethod
    def create_room(current_member, validated_data):
        room = RoomRepository.check_exist_room(
            name=validated_data['name'],
            type_=validated_data['type']
        )
        if room is None:
            room = Room.objects.create(
                name=validated_data['name'],
                type=validated_data['type']
            )
            room.add_member(current_member, room)
        return room

