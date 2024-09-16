from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(choices=[('D', 'Direct'), ('G', 'Group'), ('C', 'Channel')], max_length=1)
    # latest_message_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'room'
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.name

    def add_member(self, user):
        from . import RoomMember

        if not RoomMember.objects.filter(user_id=user.id).exists():
            RoomMember.objects.create(room=self, user=user)

