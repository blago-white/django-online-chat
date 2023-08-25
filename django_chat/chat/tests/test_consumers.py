import asyncio

from django.test import TestCase
from channels.testing import HttpCommunicator, WebsocketCommunicator

from ..consumers import ChatConsumer


class ChatConsumerTestCase(TestCase):
    _received_message: str
    _websocket_communicator: WebsocketCommunicator

    async def test_hello_message(self):
        await self._start_websocket_connection()
        self.assertEqual(await self._websocket_communicator.receive_from(), "Hello world!")

    async def _start_websocket_connection(self):
        self._websocket_communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")
        await self._websocket_communicator.connect()
