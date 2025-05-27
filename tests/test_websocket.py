import pytest
from channels.testing import WebsocketCommunicator
from sparrow.asgi import application


@pytest.mark.asyncio
@pytest.mark.django_db
class TestWebSocket:
    async def test_websocket_connect_send_receive(self):
        # 1. Create a communicator to simulate WebSocket connection
        communicator = WebsocketCommunicator(application, "/ws/chat/testroom/")
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"

        # 2. Send a message to the WebSocket
        message = {"action": "chat", "message": "Hello, world!"}
        await communicator.send_json_to(message)

        # 3. Receive the broadcasted message
        response = await communicator.receive_json_from()
        assert response["action"] == "chat"
        assert response["message"] == "Hello, world!"

        # 4. Wait for the keep-alive message (simulate 30s, but we can skip waiting in tests)
        # Optionally, you can fast-forward asyncio or patch sleep for faster tests.
        # For now, let's just check that the connection is still open.
        # (You can add more advanced keep-alive tests later.)

        # 5. Disconnect
        await communicator.disconnect()

