from django.db import models

from authorize.models import Member
from ..models import Room


class Message(models.Model):
    body = models.CharField(max_length=255)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    seen_at = models.DateTimeField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')

    class Meta:
        db_table = 'message'
        verbose_name = "Message"
        verbose_name_plural = "Messages"

