from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationStrategy:

    def send(self, room_id, message, action):
        raise NotImplementedError

class WebSocketNotification(NotificationStrategy):

    def send(self, room_id, message, action):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{room_id}',
            {
                'type': 'send_message',
                'message': message,
                'action': action,
            }
        )

# You can add more strategies later, e.g. EmailNotification, PushNotification, etc.
def notify(room_id, message, action, strategy=None):
    if strategy is None:
        strategy = WebSocketNotification()
    strategy.send(room_id, message, action)