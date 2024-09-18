from rest_framework import serializers

from authorize.serializers import UserSerializer
from ..models import RoomMember


class RoomMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for User

    class Meta:
        model = RoomMember
        fields = ['user']

