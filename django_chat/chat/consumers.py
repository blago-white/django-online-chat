import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .services import consumers


class MessageTypes:
    CREATE = "create"
    DELETE = "delete"


class ChatMessageConsumer(AsyncWebsocketConsumer):
    _MAIN_GROUP_NAME = "_"

    async def connect(self):
        await self.channel_layer.group_add(self._MAIN_GROUP_NAME, self.channel_name)
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        message: dict = json.loads(text_data)

        if message.get("type") == MessageTypes.CREATE:
            saved_message = await consumers.save_message(message=message)

            await self.channel_layer.group_send(group=self._MAIN_GROUP_NAME,
                                                message=dict(
                                                    type="chat_message",
                                                    message=json.dumps(saved_message))
                                                )

        elif message.get("type") == MessageTypes.DELETE:
            deleted = await consumers.delete_message(message=message)

            await self.channel_layer.group_send(group=self._MAIN_GROUP_NAME,
                                                message=dict(
                                                    type="chat_message",
                                                    message=json.dumps(deleted))
                                                )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self._MAIN_GROUP_NAME, self.channel_name)

    async def chat_message(self, message: dict[str, dict]):
        await self.send(message["message"])
