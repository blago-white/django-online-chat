from django.contrib.auth.models import User
from django.test import TestCase

from django_chat import tests_utils
from .. import models
from ..services import messages


class MessagesTestCase(TestCase):
    _test_message_properties: dict
    _test_message: models.Message
    _test_user: User

    def setUp(self) -> None:
        self._test_user = tests_utils.get_test_user()
        self._test_message_properties = dict(
            sender=self._test_user,
            text="Test text"
        )

    def test_get_chat_messages(self):
        self.assertFalse(bool(messages.get_chat_messages().count()))

        self._add_test_message()

        self.assertEqual(messages.get_chat_messages().count(), 1)
        self.assertEqual(messages.get_chat_messages()[0], self._test_message)

    async def test_async_save_message(self):
        await messages.async_save_message(text=self._test_message_properties["text"],
                                          from_user_id=self._test_user.pk)
        self.assertTrue(await tests_utils.check_messages_appeared())

    def _add_test_message(self):
        self._test_message = models.Message(**self._test_message_properties)
        self._test_message.save()

