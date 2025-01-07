import pytest
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from channels.layers import get_channel_layer
from apis.routing import application  # Make sure to import your ASGI application


@pytest.mark.asyncio
class WebSocketTestCase(TestCase):

    async def test_websocket_message_send(self):
        # Create a communicator to simulate WebSocket connection
        communicator = WebsocketCommunicator(application, "/ws/some_channel/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Send a message via Django Channels
        message = "Test message"
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'chat_some_channel',  # This should match the group name used in your consumer
            {
                'type': 'send_message',  # This is the method in your consumer
                'message': message
            }
        )

        # Receive the message from WebSocket
        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], message)

        # Close the connection
        await communicator.disconnect()
