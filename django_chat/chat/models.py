from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now=True)
