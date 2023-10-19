import json

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView, FormView
from django.core.handlers.asgi import ASGIRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse

from . import forms
from .services import users, urls

__all__ = ["AuthView"]


class AuthView(FormView, RedirectView):
    form_class = forms.UserRegistrationForm

    http_method_names = ["post", "head", "options", "trace"]

    def post(self, request, *args, **kwargs):
        form: forms.UserRegistrationForm = self.get_form()

        if form.is_valid():
            form.save()
            login(request=request, user=form.instance)
            return HttpResponseRedirect(redirect_to=reverse("chat"))

        elif (user := users.get_authenticated_user(request)) is not None:
            login(request=request, user=user)
            return HttpResponseRedirect(redirect_to=reverse("chat"))

        form_errors = json.loads(form.errors.as_json())

        return HttpResponseRedirect(
            redirect_to=urls.get_auth_failed_url_with_errors(errors=form_errors)
        )
