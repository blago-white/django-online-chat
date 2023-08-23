from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.OneToOneField(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now=True)
