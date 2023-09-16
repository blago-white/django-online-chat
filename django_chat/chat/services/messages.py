from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from ..models import Message


def get_chat_messages_values() -> QuerySet:
    return get_chat_messages().values()


def get_chat_messages() -> QuerySet:
    return Message.objects.all()


@sync_to_async
def async_save_message(text: str, from_user_id: int) -> None:
    new_message = Message(sender_id=from_user_id, text=text)
    new_message.full_clean()
    new_message.save()
