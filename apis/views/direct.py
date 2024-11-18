from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..entities import RoomRepository
from ..models import Room
from ..serializers import DirectSerializer


class DirectView(APIView):
    queryset = Room.objects.all()
    serializer_class = DirectSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DirectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            room = serializer.save()
            return Response(DirectSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        rooms = Room.objects.filter(room_members__member_id=request.user.id)
        serializer = self.serializer_class(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DirectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = RoomRepository.get_by_id(room_id)
        serializer = DirectSerializer(room)
        return Response(serializer.data)

