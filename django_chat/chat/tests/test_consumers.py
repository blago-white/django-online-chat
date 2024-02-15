import asyncio
import json
import time

from asgiref import sync

from channels.testing import WebsocketCommunicator
from django.test import TestCase

from common import tests_utils

from ..exceptions import NotCorrectChatMessageFormat
from ..consumers import ChatMessageConsumer
from ..models import Message


class ChatConsumerTestCase(TestCase):
    _received_message: str
    _websocket_communicator: WebsocketCommunicator

    _POLLING_TIMEOUT = 2

    async def test_receive(self):
        await self._start_websocket_connection()

        await self._websocket_communicator.send_to(
            text_data=json.dumps({"irrelevant_key": None})
        )

        self.assertFalse(await self.start_pooling_for_response())

        await self._start_websocket_connection()

        test_user = await tests_utils.async_get_test_user()

        await self._websocket_communicator.send_to(
            text_data=json.dumps(
                {"userid": test_user.pk, "message": "test message"}
            )
        )

        self.assertTrue(await self.start_pooling_for_response())

    async def start_pooling_for_response(self) -> bool:
        start = time.time()

        while time.time() - start < self._POLLING_TIMEOUT:
            messages = await tests_utils.check_messages_appeared()
            if messages:
                return messages
            else:
                await asyncio.sleep(.2)

    async def _start_websocket_connection(self):
        self._websocket_communicator = WebsocketCommunicator(ChatMessageConsumer.as_asgi(), "/ws/chat/")
        await self._websocket_communicator.connect()
