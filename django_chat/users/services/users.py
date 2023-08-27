from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.handlers.asgi import ASGIRequest


def create_user(post_request: ASGIRequest) -> User:
    user = User(username=post_request.POST.get("username"),
                password=post_request.POST.get("password1"))
    user.full_clean()
    user.save()

    return user


def get_authenticated_user(post_request: ASGIRequest) -> User | None:
    return authenticate(request=post_request,
                        username=post_request.POST.get("username"),
                        password=post_request.POST.get("password1"))
