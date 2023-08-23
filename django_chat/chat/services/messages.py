from django.db.models import QuerySet
from ..models import Message


def get_chat_messages() -> QuerySet:
    return Message.objects.all()
