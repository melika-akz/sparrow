import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now
from asgiref.sync import sync_to_async
from apis.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles new WebSocket connections"""
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming WebSocket messages"""
        data = json.loads(text_data)
        action = data.get("action")

        if action == "message_seen":
            message_id = data.get("message_id")
            user_id = self.scope["user"].id  # Get the user ID from the WebSocket scope
            await self.mark_message_as_seen(message_id, user_id)

    async def mark_message_as_seen(self, message_id, user_id):
        """Marks a message as seen and notifies the sender"""
        message = await sync_to_async(Message.objects.filter)(id=message_id)
        message = await sync_to_async(message.first)()

        if message and message.sender.id != user_id:
            message.seen_at = now()
            await sync_to_async(message.save)()

            # Notify the sender
            await self.channel_layer.group_send(
                f"chat_{message.room.id}",
                {
                    "type": "chat.message.seen",
                    "message_id": message.id,
                    "seen_at": message.seen_at.isoformat(),
                    "seen_by": user_id
                }
            )

    async def chat_message_seen(self, event):
        """Sends a seen notification to the WebSocket clients"""
        await self.send(text_data=json.dumps({
            "action": "message_seen",
            "message_id": event["message_id"],
            "seen_at": event["seen_at"],
            "seen_by": event["seen_by"]
        }))

    async def chat_message(self, event):
        """Sends message data to WebSocket clients"""
        await self.send(json.dumps(event["message"]))  # Send full message data
