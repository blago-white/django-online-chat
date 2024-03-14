from typing import Callable

from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class UserLoggedInMiddleware:
    _ADMIN_PANEL_URL: str = settings.ADMIN_PANEL_URL
    _API_URL: str = settings.API_URL
    _CHAT_PAGE_URL: str = reverse_lazy("chat")
    _AUTH_URL: str = reverse_lazy("home")

    _STATELESS_URLS: tuple = _API_URL, _ADMIN_PANEL_URL

    def __init__(self, get_response: Callable):
        self._get_response = get_response

    def __call__(self, request: ASGIRequest):
        if any(request.path.startswith(stateless_url) for stateless_url in self._STATELESS_URLS):
            return self._get_response(request)

        path_is_chat_page = request.path == self._CHAT_PAGE_URL

        if request.user.is_authenticated and not path_is_chat_page:
            return HttpResponseRedirect(redirect_to=self._CHAT_PAGE_URL)

        elif not request.user.is_authenticated and path_is_chat_page:
            return HttpResponseRedirect(redirect_to=self._AUTH_URL)

        return self._get_response(request)
