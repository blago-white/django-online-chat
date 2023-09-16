from . import messages
from .. import exceptions


async def save_message(message: dict) -> None:
    try:
        userid, message = _get_user_message_payload(from_client_message=message)
    except:
        raise exceptions.NotCorrectChatMessageFormat

    await messages.async_save_message(from_user_id=userid, text=message)


def _get_user_message_payload(from_client_message: dict) -> tuple[int, str]:
    return int(from_client_message["userid"]), from_client_message["message"]
