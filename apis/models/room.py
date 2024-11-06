from django.db import models

from authorize.models import Member


class Room(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(choices=[('D', 'Direct'), ('G', 'Group'), ('C', 'Channel')], max_length=1)
    members = models.ManyToManyField(Member, through='RoomMember', related_name='rooms')
    # latest_message_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'room'
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.name

    def add_member(self, user, room):
        from . import RoomMember

        if not RoomMember.objects.filter(user_id=user.id, room_id=room.id).exists():
            RoomMember.objects.create(room=self, user=user)

