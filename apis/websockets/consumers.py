import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import logging


logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat_{self.room_id}'

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        self.keep_alive_task = asyncio.create_task(self.send_keep_alive())


    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        action = text_data_json.get('action')

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'message': message,
                'action': action,
            }
        )

    async def send_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'message': event['message']
        }))

    async def send_keep_alive(self):
        while True:
            await asyncio.sleep(30)
            await self.send(text_data=json.dumps({
                'action': 'answer',
                'message': 'keep-alive',
            }))

