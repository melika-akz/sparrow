from django.db import models

from authorize.models import Member

from . import Room, Message


class RoomMember(models.Model):
    room = models.ForeignKey(Room, related_name='room_members', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    latest_seen_message = models.ForeignKey(
        Message,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="seen_by_members",
        help_text="The last message seen by the member in this room"
    )
    latest_seen_message_created_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of the last message seen by the member"
    )

    class Meta:
        db_table = 'room_member'
        verbose_name = "Room Member"
        verbose_name_plural = "Room Members"

