from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Room
from ..serializers import DirectSerializer


class DirectView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = DirectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(room_members__member=self.request.user).distinct().prefetch_related('room_members')


class DirectDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = DirectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(Room, id=self.kwargs['room_id'])

