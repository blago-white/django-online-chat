from django.core.handlers.asgi import ASGIRequest
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from users.forms import UserRegistrationForm
from .services import messages

__all__ = ["MessagesAPIView", "home_view", "chat_view"]


class MessagesAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response({"messages": messages.get_chat_messages_values()})


def home_view(request: ASGIRequest):
    context = dict(register_form=UserRegistrationForm)

    if form_errors := request.GET.getlist("error"):
        context.update(errors=form_errors)

    return render(request=request, template_name="chat/home.html", context=context)


def chat_view(request: ASGIRequest):
    context = dict(messages=messages.get_chat_messages())

    return render(request=request, template_name="chat/chat.html", context=context)
