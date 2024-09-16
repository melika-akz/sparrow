from django.db import models


class Message(models.Model):
    body = models.CharField(max_length=255)
    sender_id = models.CharField(max_length=255)

