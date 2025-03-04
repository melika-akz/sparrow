from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorator import send_websocket_message
from ..models import Message, Room, RoomMember
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


class MessageSeenView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, message_id):

        try:
            member = request.user

            # Validate message
            message = Message.objects.get(id=message_id, room__room_members__member=member)

            if message.sender_id == member.id:
                return Response(
                    {"error": "You cannot mark your own message as seen"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update the RoomMember's latest seen message
            room_member = RoomMember.objects.get(room=message.room, member=member)
            room_member.latest_seen_message = message
            room_member.latest_seen_message_created_at = message.created_at
            room_member.save()

            # Update message seen status
            if member not in message.seen_by.all():
                message.seen_by.add(member)
                if not message.seen_at:  # Set seen_at only once
                    message.seen_at = message.created_at
                message.save()
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Message.DoesNotExist:
            return Response({"error": "Message not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        except RoomMember.DoesNotExist:
            return Response({"error": "User is not a member of the room"}, status=status.HTTP_403_FORBIDDEN)

