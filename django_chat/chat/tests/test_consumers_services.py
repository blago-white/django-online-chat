import json

from django.test import TestCase

from ..services import consumers_services


class ConsumersServicesTestCase(TestCase):
    _TEST_MESSAGE_USERID = "1"
    _TEST_MESSAGE_TEXT = "test message"
    _TEST_JSON_MESSAGE = json.dumps({"userid": _TEST_MESSAGE_USERID,
                                     "message": _TEST_MESSAGE_TEXT})

    def test_get_user_message_payload(self):
        self.assertEqual(consumers_services.get_user_message_payload(text_data=self._TEST_JSON_MESSAGE),
                         (int(self._TEST_MESSAGE_USERID), self._TEST_MESSAGE_TEXT))
