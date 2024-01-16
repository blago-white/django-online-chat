from django.contrib.auth.models import User
import django.forms as forms
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=8, label="username")
    password1 = forms.CharField(max_length=12, min_length=8, label="password")
    password2 = None

    class Meta:
        model = User
        fields = ["username"]
