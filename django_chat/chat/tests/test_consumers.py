import json

from channels.testing import WebsocketCommunicator
from django.test import TestCase

from django_chat import tests_utils
from ..consumers import ChatMessageConsumer


class ChatConsumerTestCase(TestCase):
    _received_message: str
    _websocket_communicator: WebsocketCommunicator

    async def test_receive(self):
        await self._start_websocket_connection()

        await self._websocket_communicator.send_to(
            text_data=json.dumps({"irrelevant_key": None})
        )

        self.assertFalse(await tests_utils.check_messages_appeared())

        await self._websocket_communicator.send_to(
            text_data=json.dumps({"userid": (await tests_utils.async_get_test_user()).pk, "message": "test message"})
        )

        self.assertTrue(await tests_utils.check_messages_appeared())

    async def _start_websocket_connection(self):
        self._websocket_communicator = WebsocketCommunicator(ChatMessageConsumer.as_asgi(), "/ws/chat/")
        await self._websocket_communicator.connect()
