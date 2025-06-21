from rest_framework import serializers

from messenger.models import Room


class MemberRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'name', 'type']

