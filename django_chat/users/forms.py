import django.forms as forms
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="password")
    password2 = forms.CharField(label="repeat password")
