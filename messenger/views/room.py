from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from ..constants import DIRECT
from ..models import Room
from ..serializers import RoomSerializer, RoomDetailSerializer


class RoomView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(members=user).prefetch_related('room_members').exclude(type=DIRECT)


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.prefetch_related('room_members')

    def get_object(self):
        room = get_object_or_404(self.get_queryset(), id=self.kwargs['room_id'])
        if not room.room_members.filter(member=self.request.user).exists():
            raise PermissionDenied("You do not have permission to access this room.")
        return room

