from django.core.handlers.asgi import ASGIRequest
from django.shortcuts import render
from users.forms import UserRegistrationForm

from .services import messages


__all__ = ["home_view", "chat_view"]


def home_view(request: ASGIRequest):
    context = dict(register_form=UserRegistrationForm)

    return render(request=request, template_name="chat/home.html", context=context)


def chat_view(request: ASGIRequest):
    context = dict(messages=messages.get_chat_messages())

    return render(request=request, template_name="chat/chat.html", context=context)
