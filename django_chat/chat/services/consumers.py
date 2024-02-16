from django.forms.models import model_to_dict

from . import messages
from .. import exceptions


async def save_message(message: dict) -> None:
    try:
        userid, message_text = get_message_data(
            payload=get_user_message_payload(
                from_client_message=message
            )
        )
    except:
        raise exceptions.NotCorrectChatMessageFormat(message)

    created = await messages.async_save_message(text=message_text, from_user_id=userid)

    message["payload"].update(message_id=created.pk)

    return message


async def delete_message(message: dict) -> dict:
    try:
        message_id = get_message_id(
            get_user_message_payload(
               from_client_message=message
            )
        )
    except:
        raise exceptions.NotCorrectChatMessageFormat(message)

    await messages.async_delete_message(message_id=message_id)

    return message


def get_user_message_payload(from_client_message: dict) -> dict:
    return from_client_message.get("payload")


def get_message_data(payload: dict) -> tuple[int, str]:
    return int(payload["userid"]), payload["message"]


def get_message_id(payload: dict) -> tuple[int, str]:
    return int(payload["message_id"])
