from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .serializers import CommentSerializer


def notify_consumers(comment, method, group):
    serialized_data = CommentSerializer(comment).data
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group,
            {
                "type": method,
                "data": serialized_data
            }
        )
    except Exception as e:
        pass