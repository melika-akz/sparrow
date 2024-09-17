from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import OuterRef, Subquery
from rest_framework import serializers

from authorize.models import User
from .room_member import RoomMemberSerializer
from ..models import Room


class RoomSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)
    members = RoomMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['members', 'member_id']

    def validate(self, data):
        member_id = data.get('member_id')
        if member_id == self.context['request'].user.id:
            raise serializers.ValidationError('You cannot create a room to chat with yourself.')
        return data

    def create(self, validated_data):
        member_id = validated_data.pop('member_id')
        current_member = self.context['request'].user
        member = User.objects.filter(id=member_id).first()
        if member is None:
            raise serializers.ValidationError('Member Not Exist')

        direct = self.check_exist_room(destination_id=member_id, source_id=current_member.id)
        room = super().create(validated_data)
        room.add_member(current_member)
        room.add_member(member)
        return room

    def check_exist_room(self, destination_id, source_id):
        from ..models import RoomMember

        # Subquery to get the CTE results
        cte_subquery = RoomMember.objects.filter(
            room_id=OuterRef('pk'),
        ).values('room_id').annotate(
            members=ArrayAgg('user_id', ordering=['user_id'])
        ).values('members')

        # Query to filter Directs based on the CTE results
        direct = Room.objects.filter(
            id__in=Subquery(cte_subquery),
            type='Direct',
            roommember__members=sorted([source_id, destination_id])
        ).distinct().first()

        return direct