import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    _MAIN_GROUP_NAME = "main"
    _TEST_MESSAGE = {
        "type": "hello_message",
        "message": "Hello world!"
    }

    async def connect(self):
        await self.channel_layer.group_add(
            self._MAIN_GROUP_NAME,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self._MAIN_GROUP_NAME,
            self._TEST_MESSAGE
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self._MAIN_GROUP_NAME,
            self.channel_name
        )

    async def hello_message(self, event):
        await self.send(text_data=self._TEST_MESSAGE["message"])
