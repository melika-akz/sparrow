from django.db import models

from authorize.models import User
from . import Room


class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

