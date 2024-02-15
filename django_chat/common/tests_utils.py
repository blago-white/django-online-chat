import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.core.handlers.asgi import ASGIRequest

from chat.models import Message
from . import tests_config


def get_test_post_request(url: str = "/", make_user_authenticated: bool = False, **request_data) -> ASGIRequest:
    request = ASGIRequest(dict(path=url, method="post"), None)

    request.user = User() if make_user_authenticated else AnonymousUser()

    for param_name in request_data:
        request.__dict__[param_name] = request_data[param_name]

    return request


@sync_to_async
def async_get_test_user() -> User:
    return User.objects.create_user(
        username=tests_config.TEST_USER_USERNAME,
        password=tests_config.TEST_USER_PASSWORD
    )


def get_test_user() -> User:
    return User.objects.create_user(
        username=tests_config.TEST_USER_USERNAME,
        password=tests_config.TEST_USER_PASSWORD
    )


async def check_messages_appeared() -> bool:
    return await Message.objects.acount()
