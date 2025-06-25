from enum import Enum
from django.db import models

from .mixins import MemberStampedModel
from ..constants import ROOM_TYPES
from authorize.models import Member


class TypeChoices(Enum):

    @classmethod
    def choices(cls):
        return [(choice, choice.capitalize()) for choice in ROOM_TYPES]


class Room(MemberStampedModel, models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(choices=TypeChoices.choices(), max_length=7)
    members = models.ManyToManyField(Member, through='RoomMember', related_name='rooms')
    latest_message_id = models.ForeignKey('Message', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    class Meta:
        db_table = 'room'
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.name

    def add_member(self, member):
        from . import RoomMember

        if not RoomMember.objects.filter(member_id=member.id, room_id=self.id).exists():
            RoomMember.objects.create(room=self, member=member)

    def remove_member(self, member):
        from . import RoomMember
        RoomMember.objects.filter(member_id=member.id, room_id=self.id).delete()
