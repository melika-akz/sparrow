from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(choices=[('D', 'Direct'), ('G', 'Group'), ('C', 'Channel')], max_length=1)
    # latest_message_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name