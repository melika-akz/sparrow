from rest_framework import serializers

from authorize.serializers import MemberSerializer

from ..models import RoomMember


class RoomMemberSerializer(serializers.ModelSerializer):
    user = MemberSerializer()  # Nested serializer for User

    class Meta:
        model = RoomMember
        fields = ['user']

