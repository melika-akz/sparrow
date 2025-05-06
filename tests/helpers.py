import json
import asyncio
from channels.testing import WebsocketCommunicator
from sparrow.asgi import application
from rest_framework.test import APITransactionTestCase


def _client(
        test_case: APITransactionTestCase,
        method: str,
        path: str,
        data: dict = None
):
    """Custom client function to handle API requests.

    Args:
        test_case (APITransactionTestCase): An instance of APITransactionTestCase for making requests.
        method (str): The HTTP method (e.g., 'POST', 'PUT', 'PATCH', 'DELETE').
        path (str): The API endpoint to request.
        data (dict, optional): The data to send with the request. Defaults to None.

    Returns:
        Response: The response from the API.
    """
    if data is not None:
        data = json.dumps(data)

    response = test_case.client.generic(
        method,
        path,
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

