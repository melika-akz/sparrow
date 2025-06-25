import json
import ujson
import asyncio
from channels.testing import WebsocketCommunicator

from authorize.helpers import generate_jwt_token
from sparrow.asgi import application
from rest_framework.test import APITransactionTestCase


class BaseTestCase(APITransactionTestCase):
    def login(self, user):
        self.jwt_token = generate_jwt_token(user)
        self.client.force_authenticate(user=user, token=self.jwt_token)

    def logout(self):
        self.client.force_authenticate(user=None)
        self.jwt_token = None

    def _client(self, text: str, method: str, path: str, data: dict = None):
        if data is not None:
            data = json.dumps(data)
        else:
            data = json.dumps({})

        response = self.client.generic(
            method=method.upper(),
            path=path,
            data=data,
            content_type='application/json'
        )
        return response


def async_run(coro):
    """Runs an asynchronous coroutine in a synchronous context.

    Args:
        coro (coroutine): The coroutine to run.

    Returns:
        Any: The result of the coroutine.
    """
    return asyncio.get_event_loop().run_until_complete(coro)


class WebSocketTestHelper:
    def __init__(self, room_id):
        self.room_id = room_id
        self.communicator = WebsocketCommunicator(application, f"/ws/chat/{room_id}/")
        self.connected = False

    def connect(self):
        self.connected, _ = async_run(self.communicator.connect())
        return self.connected

    def receive_json(self):
        return async_run(self.communicator.receive_json_from())

    def disconnect(self):
        async_run(self.communicator.disconnect())

