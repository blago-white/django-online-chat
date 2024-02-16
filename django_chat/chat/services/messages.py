from asgiref.sync import sync_to_async
from django.db.models import QuerySet, Model

from ..models import Message


def get_chat_messages_values() -> QuerySet:
    return get_chat_messages().values()


def get_chat_messages() -> QuerySet:
    return Message.objects.all()


async def async_save_message(text: str, from_user_id: int) -> Message:
    return await Message.objects.acreate(sender_id=from_user_id, text=text)


@sync_to_async
def async_delete_message(message_id: int) -> None:
    return Message.objects.filter(pk=message_id).delete()
