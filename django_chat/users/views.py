from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.asgi import ASGIRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse

from .services import users

__all__ = ["signup_view", "login_view"]


def signup_view(request: ASGIRequest):
    try:
        new_user = users.create_user(post_request=request)
        login(request=request, user=new_user)
    except:
        return HttpResponseRedirect(redirect_to=reverse("home"))

    return HttpResponseRedirect(redirect_to=reverse("chat"))


def login_view(request: ASGIRequest):
    if request.method == "POST":
        return _process_login_form_view(request=request)

    return _get_login_form_view(request=request)


def _get_login_form_view(request: ASGIRequest):
    context = dict(login_form=AuthenticationForm)

    return render(request=request, template_name="users/login.html", context=context)


def _process_login_form_view(request: ASGIRequest):
    user = users.get_authenticated_user(post_request=request)

    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(redirect_to=reverse("chat"))

    return _get_login_form_view(request=request)
