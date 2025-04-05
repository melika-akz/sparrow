from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Message, Room, RoomMember
from ..serializers import MessageSerializer


class MessageView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['body']

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        cache_key = f"messages_room_{room_id}"

        messages = cache.get(cache_key)
        if messages is not None:
            return messages

        get_object_or_404(Room, id=room_id)
        messages = Message.objects.filter(room_id=room_id).select_related('sender', 'room').order_by('-created_at')
        print(messages)
        for m in messages:
            print(m.body)

        cache.set(cache_key, messages, timeout=300)  # Cache for 5 minutes
        return messages

    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_id')
        room = get_object_or_404(Room, id=room_id)

        serializer.save(sender=self.request.user, room=room)
        cache.delete(f"messages_room_{room_id}")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        room_id = self.kwargs.get('room_id')
        context['room'] = get_object_or_404(Room, id=room_id)
        return context

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{self.kwargs.get("room_id")}',
            {
                'type': 'send_message',
                'message': response.data,
                'action': 'send',
            }
        )
        return response


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

            # Send WebSocket message to notify others that the message has been seen
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{message.room.id}',  # The group name based on room
                {
                    'type': 'send_message',  # Custom event to send to WebSocket
                    'message': serializer.data,
                    'action': 'seen',
                }
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Message.DoesNotExist:
            return Response({"error": "Message not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

        except RoomMember.DoesNotExist:
            return Response({"error": "User is not a member of the room"}, status=status.HTTP_403_FORBIDDEN)

