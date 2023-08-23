from django.shortcuts import render
from .services import messages


def home_view(request):
    return render(request=request, template_name="chat/home.html")


def chat_view(request):
    context = dict(
        messages=messages.get_chat_messages()
    )

    return render(request=request, template_name="chat/chat.html", context=context)
