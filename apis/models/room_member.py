from django.db import models

from authorize.models import User
from . import Room


class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_member'
        unique_together = ('room', 'user')
        verbose_name = "Room Member"
        verbose_name_plural = "Room Members"

