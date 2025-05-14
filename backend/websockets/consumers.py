import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.channel_layer.group_add("comments", self.channel_name)
            await self.accept()
        except Exception:
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("comments", self.channel_name)
        except Exception:
            pass

    async def comment_created(self, event):
        try:
            await self.send(text_data=json.dumps({
                'type': 'new_comment',
                'data': event['data']
            }))
        except Exception:
            pass
