from channels.routing import URLRouter
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import SimpleTestCase, override_settings
from websockets.routing import websocket_urlpatterns

channel_layers = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


@override_settings(CHANNEL_LAYERS=channel_layers)
class CommentConsumerTest(SimpleTestCase):

    async def test_websocket_consumer(self):
        application = URLRouter(websocket_urlpatterns)
        communicator = WebsocketCommunicator(application, "ws/comments/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        channel_layer = get_channel_layer()
        await channel_layer.group_send("comments", {
            "type": "comment_created",
            "data": {"id": 999, 'text': 'test message'},
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_comment")
        await communicator.disconnect()
