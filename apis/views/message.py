from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..decorator import send_websocket_message
from ..models import Message, Room
from ..serializers import MessageSerializer


class MessageView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        get_object_or_404(Room, id=room_id)
        return Message.objects.filter(room_id=room_id).select_related('sender', 'room').order_by('created_at')

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)

        serializer.save(sender=self.request.user, room=room)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        room_id = self.kwargs.get('room_id')
        context['room'] = get_object_or_404(Room, id=room_id)
        return context

    @send_websocket_message('chat_some_channel')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return Message.objects.filter(room_id=room_id).select_related('sender', 'room')

