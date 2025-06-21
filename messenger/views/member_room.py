from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..constants import DIRECT
from ..models import Room
from ..serializers import MemberRoomSerializer


class MemberRoomView(generics.ListAPIView):
    serializer_class = MemberRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(members=user).prefetch_related('room_members').exclude(type=DIRECT)

