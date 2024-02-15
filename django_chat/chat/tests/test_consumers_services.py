import json

from django.test import TestCase

from ..services import consumers


class ConsumersServicesTestCase(TestCase):
    _TEST_MESSAGE_USERID = "1"
    _TEST_MESSAGE_TEXT = "test message"
    _TEST_JSON_MESSAGE = {"userid": _TEST_MESSAGE_USERID,
                          "message": _TEST_MESSAGE_TEXT}

    def test_get_user_message_payload(self):
        self.assertEqual(consumers.get_user_message_payload(
            from_client_message=self._TEST_JSON_MESSAGE
        ), (int(self._TEST_MESSAGE_USERID), self._TEST_MESSAGE_TEXT)
        )
