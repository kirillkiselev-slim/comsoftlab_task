import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "progress_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "progress_group",
            self.channel_name
        )

    async def progress_update(self, event):
        stage = event['stage']
        progress = event['progress']

        await self.send(text_data=json.dumps({
            'stage': stage,
            'progress': progress,
        }))