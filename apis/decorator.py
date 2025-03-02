import asyncio
from functools import wraps
from channels.layers import get_channel_layer

def send_websocket_message(channel_name):
    """Decorator to send message data over WebSocket after API call."""

    def decorator(func):

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)
            if response.status_code == 201:
                message_data = response.data  # the serialized message data
                room_id = kwargs.get('room_id')

                async def send_message():
                    channel_layer = get_channel_layer()
                    await channel_layer.group_send(
                        f"chat_{room_id}",  # target group name
                        {
                            "type": "chat.message",  # handler type in consumers
                            "message": message_data,
                        }
                    )

                # Try to get an already running loop.
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None

                if loop and loop.is_running():
                    # If there's a running loop (e.g. in an async context), schedule the task.
                    asyncio.create_task(send_message())
                else:
                    # Otherwise, run the coroutine in a new event loop.
                    asyncio.run(send_message())

            return response
        return wrapper
    return decorator

