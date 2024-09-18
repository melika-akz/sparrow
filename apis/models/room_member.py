from django.db import models
from django.db.models import UniqueConstraint

from authorize.models import User
from . import Room


class RoomMember(models.Model):
    room = models.ForeignKey(Room, related_name='room_members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_member'
        verbose_name = "Room Member"
        verbose_name_plural = "Room Members"
