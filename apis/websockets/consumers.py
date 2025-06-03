import logging
import asyncio
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now

from apis.models import Message

# Configure logger at module level
logger = logging.getLogger('apis.websockets.consumers')
logger.setLevel(logging.DEBUG)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles new WebSocket connections"""
        if self.scope["user"].is_anonymous:
            logger.debug("Anonymous user connection rejected")
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        logger.debug(f"User {self.scope['user'].id} connecting to room {self.room_id}")

        # Start keep-alive task
        self.keep_alive_task = asyncio.create_task(self.keep_alive())

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        logger.debug(f"Connection established for user {self.scope['user'].id} in room {self.room_id}")

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection"""
        # Cancel keep-alive task
        if hasattr(self, 'keep_alive_task'):
            self.keep_alive_task.cancel()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming WebSocket messages"""
        data = json.loads(text_data)
        action = data.get("action")

        if action == "keep-alive":
            await self.send(text_data=json.dumps({"status": "alive"}))

        if action == "message_seen":
            message_id = data.get("message_id")
            user_id = self.scope["user"].id  # Get the user ID from the WebSocket scope
            await self.mark_message_as_seen(message_id, user_id)

    async def keep_alive(self):
        """Sends a keep-alive message every 30 seconds"""
        while True:
            await asyncio.sleep(30)  # Adjust the interval if needed
            await self.send(text_data=json.dumps({"action": "keep-alive"}))

    async def mark_message_as_seen(self, message_id, user_id):
        """Marks a message as seen and notifies the sender"""
        message = await sync_to_async(Message.objects.filter)(id=message_id)
        message = await sync_to_async(message.first)()

        if message and message.sender_id != user_id:
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
        """Handles incoming chat messages"""
        logger.debug("=" * 50)
        logger.debug("Received chat_message event")
        logger.debug(f"Event data: {event}")
        
        try:
            message_data = {
                "action": "new_message",
                "message": event["message"]
            }
            logger.debug(f"Preparing to send message: {message_data}")
            
            await self.send(text_data=json.dumps(message_data))
            logger.debug("Message sent successfully to WebSocket")
            
        except Exception as e:
            logger.exception(f"Error in chat_message: {str(e)}")
            logger.error(f"Full event data that caused error: {event}")
