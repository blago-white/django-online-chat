from typing import Callable

from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class UserLoggedInMiddleware:
    _ADMIN_PANEL_URL: str = settings.ADMIN_PANEL_URL
    _CHAT_PAGE_URL: str = reverse_lazy("chat")
    _SIGNUP_URL: str = reverse_lazy("signup")

    def __init__(self, get_response: Callable):
        self._get_response = get_response

    def __call__(self, request: ASGIRequest):
        if request.path.startswith(self._ADMIN_PANEL_URL):
            return self._get_response(request)

        try:
            user_authenticated: bool = request.user.is_authenticated
        except AttributeError:
            user_authenticated: bool = False

        path_is_chat_page = request.path == self._CHAT_PAGE_URL

        if user_authenticated and not path_is_chat_page:
            return HttpResponseRedirect(redirect_to=self._CHAT_PAGE_URL)

        elif not user_authenticated and path_is_chat_page:
            return HttpResponseRedirect(redirect_to=self._SIGNUP_URL)

        return self._get_response(request)
