from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory

from django_chat import tests_utils, tests_config
from ..services import users


class UsersServiceTestCase(TestCase):
    _request_factory: RequestFactory

    def setUp(self) -> None:
        self._request_factory = RequestFactory()

    def test_create_user(self):
        not_correct_chars_username = tests_config.TEST_NOT_CORRECT_USER_USERNAME

        with self.assertRaises(ValidationError):
            users.create_user(
                post_request=self._request_factory.post(
                    path="/", data=dict(username=str(), password1=tests_config.TEST_USER_PASSWORD)
                )
            )

        with self.assertRaises(ValidationError):
            users.create_user(
                post_request=self._request_factory.post(
                    path="/", data=dict(username=not_correct_chars_username, password1=tests_config.TEST_USER_PASSWORD)
                )
            )

        with self.assertRaises(ValidationError):
            users.create_user(
                post_request=self._request_factory.post(
                    path="/", data=dict(username=tests_config.TEST_USER_USERNAME, password1=str())
                )
            )

        users.create_user(
            post_request=self._request_factory.post(
                path="/", data=dict(username=tests_config.TEST_USER_USERNAME, password1=tests_config.TEST_USER_PASSWORD)
            )
        )

        self.assertTrue(User.objects.all().exists())

        self.assertEqual(User.objects.first().username, tests_config.TEST_USER_USERNAME)

    def test_get_authenticated_user(self):
        self.assertIsNone(users.get_authenticated_user(
            post_request=self._request_factory.post(path="/")
        ))

        self.assertIsNone(users.get_authenticated_user(
            post_request=self._request_factory.post(path="/", data=dict(username=tests_config.TEST_USER_USERNAME,
                                                                        password1=tests_config.TEST_USER_PASSWORD))
        ))

        tests_utils.get_test_user()
        self.client.login(username=tests_config.TEST_USER_USERNAME, password=tests_config.TEST_USER_PASSWORD)

        self.assertEqual(users.get_authenticated_user(
            post_request=self._request_factory.post(
                path="/",
                data=dict(username=tests_config.TEST_USER_USERNAME, password1=tests_config.TEST_USER_PASSWORD),
            )
        ), User.objects.get(username=tests_config.TEST_USER_USERNAME))
