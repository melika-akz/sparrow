from functools import wraps
from channels.layers import get_channel_layer
from django.http import JsonResponse


def send_websocket_message(group_name, message_key='message'):
    """
    Decorator to send a message to a WebSocket group.

    :param group_name: The WebSocket group name to send the message to
    :param message_key: The key for the message in the view's request data (defaults to 'message')
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Get the message from the request
            message = request.data.get(message_key)
            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)

            # Send the message to the WebSocket (via channel layer)
            channel_layer = get_channel_layer()
            channel_layer.group_send(
                group_name,  # WebSocket group name
                {
                    'type': 'send_message',  # Method to call in the consumer
                    'message': message
                }
            )

            # Call the original view function
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
