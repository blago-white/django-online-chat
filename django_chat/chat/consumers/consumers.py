import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.services import consumers, base

from ._messages import MessageType
from chat import django_logger


__all__ = ["ChatMessageConsumer"]


class ChatMessageConsumer(AsyncWebsocketConsumer):
    _MAIN_GROUP_NAME = "_"
    _service: base.BaseService

    def __init__(self, *args, service=consumers.MessageService(), **kwargs):
        self._service = service
        super().__init__(*args, **kwargs)

    async def connect(self):
        print("Add channel into group")
        django_logger.debug("Add channel into group")

        await self.channel_layer.group_add(self._MAIN_GROUP_NAME, self.channel_name)
        await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        message: dict = json.loads(text_data)

        django_logger.debug(f"Receive message from WS: {message}")

        if message.get("type") == MessageType.CREATE.value:
            saved_message = await self._service.save(message=message)

            await self.channel_layer.group_send(group=self._MAIN_GROUP_NAME,
                                                message=dict(
                                                    type="chat_message",
                                                    message=json.dumps(saved_message))
                                                )

        elif message.get("type") == MessageType.DELETE.value:
            deleted = await self._service.delete(message=message)

            await self.channel_layer.group_send(group=self._MAIN_GROUP_NAME,
                                                message=dict(
                                                    type="chat_message",
                                                    message=json.dumps(deleted))
                                                )

    async def disconnect(self, code):
        django_logger.debug(f"Disconnect channel from group")

        await self.channel_layer.group_discard(self._MAIN_GROUP_NAME, self.channel_name)

    async def chat_message(self, message: dict[str, dict]):
        print("WS Message send to client")
        django_logger.debug(f"WS Message send to client")

        await self.send(message["message"])
