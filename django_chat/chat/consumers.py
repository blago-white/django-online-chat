import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .services import consumers_services


class ChatMessageConsumer(AsyncWebsocketConsumer):
    _MAIN_GROUP_NAME = "_"

    async def connect(self):
        await self.channel_layer.group_add(self._MAIN_GROUP_NAME, self.channel_name)
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        message: dict = json.loads(text_data)

        print(message, '-----')

        await consumers_services.save_message(message=message)

        print('---------1121')

        await self.channel_layer.group_send(group=self._MAIN_GROUP_NAME,
                                            message=dict(type="chat_message", message=json.dumps(message)))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self._MAIN_GROUP_NAME, self.channel_name)

    async def chat_message(self, message: dict[str, dict]):
        await self.send(message["message"])
