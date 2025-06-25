from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..entities import RoomMemberFacade
from ..models import Room


class RoomMemberJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        member = request.user

        RoomMemberFacade(room, member).operation_join()

        return Response(status=status.HTTP_200_OK)


class RoomMemberLeaveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        member = request.user

        RoomMemberFacade(room, member).operation_leave()

        return Response( status=status.HTTP_200_OK)


class RoomMemberAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        member = request.user
        members = request.data.get("members", [])

        RoomMemberFacade(room, member).operation_add(members)

        return Response(status=status.HTTP_200_OK)


class RoomMemberRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        member = request.user
        members = request.data.get("members", [])

        RoomMemberFacade(room, member).operation_remove(members)
        return Response(status=status.HTTP_200_OK)

