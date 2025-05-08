from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/comments/", consumers.CommentConsumer.as_asgi()),
]
