from django.db import models

from authorize.models import Member

from . import Room


class RoomMember(models.Model):
    room = models.ForeignKey(Room, related_name='room_members', on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_member'
        verbose_name = "Room Member"
        verbose_name_plural = "Room Members"

