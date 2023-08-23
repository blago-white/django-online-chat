from django.test import TestCase
from django.contrib.auth.models import User

from ..services import messages

from . import testing_utils
from .. import models


class MessagesTestCase(TestCase):
    _test_message_properties: dict
    _test_message: User

    def setUp(self) -> None:
        self._test_message_properties = dict(
            sender=testing_utils.get_test_user(),
            text="Test text"
        )

    def test_get_chat_messages(self):
        self.assertFalse(bool(messages.get_chat_messages().count()))

        self._add_test_message()

        self.assertEqual(messages.get_chat_messages().count(), 1)
        self.assertEqual(messages.get_chat_messages()[0], self._test_message)

    def _add_test_message(self):
        self._test_message = models.Message(**self._test_message_properties)
        self._test_message.save()
