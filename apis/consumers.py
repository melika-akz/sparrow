import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'some_channel'
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from the WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  # Parse the incoming JSON data
        message = text_data_json['message']     # Extract the message field

        # Now, send this message back to WebSocket (or to other clients)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Function to handle sending messages from the backend
    async def send_message(self, event):
        # Send message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
