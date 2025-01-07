from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..decorator import send_websocket_message
from ..models import Message, Room
from ..serializers import MessageSerializer


class MessageView(APIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, room_id):
        try:
            return Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise NotFound(detail="Room not found")

    @send_websocket_message('chat_some_channel')
    def post(self, request, room_id):
        room = self.get_object(room_id)
        serializer = MessageSerializer(data=request.data, context={'request': request, 'room': room})
        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return Response(MessageSerializer(message).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, room_id):
        self.get_object(room_id)
        messages = Message.objects.filter(room__id=room_id, sender__id=request.user.id)
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

