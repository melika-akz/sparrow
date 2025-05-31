from django.db.models import OuterRef, Subquery, Count, IntegerField, F, Q, Sum
from django.shortcuts import get_object_or_404
from requests.utils import set_environ
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce


from ..constants import DIRECT
from ..models import Room, RoomMember, Message
from ..serializers import RoomSerializer, RoomDetailSerializer, UnreadCountSerializer


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


class UnreadCountView(generics.ListAPIView):
    serializer_class = UnreadCountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        unread_subquery = Message.objects \
            .filter(room_id=OuterRef('room_id')) \
            .filter(
                ~Q(sender_id=self.request.user.id),
                Q(id__gt=Coalesce(OuterRef('latest_seen_message__id'), 0))
            ) \
            .values('room_id') \
            .annotate(unread_count=Count('id')) \
            .values('unread_count')

        unread_count = RoomMember.objects \
            .filter(member=self.request.user) \
            .annotate(
                unread_count=Subquery(unread_subquery, output_field=IntegerField()),
                room_type=F('room__type')
            ) \
            .values(room_type=F('room__type')) \
            .annotate(total_unread=Coalesce(Sum('unread_count'), 0))
        return unread_count

