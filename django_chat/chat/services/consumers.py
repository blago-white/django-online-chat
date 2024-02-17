from django.forms.models import model_to_dict

from . import messages, _utils
from .. import exceptions


class MessageService:
    async def save(self, message: dict) -> dict:
        try:
            userid, message_text = _utils.get_message_data(
                payload=_utils.get_user_message_payload(
                    from_client_message=message
                )
            )
        except:
            raise exceptions.NotCorrectChatMessageFormat(message)

        created = await messages.async_save_message(text=message_text, from_user_id=userid)

        message["payload"].update(message_id=created.pk)

        return message

    async def delete(self, message: dict) -> dict:
        try:
            message_id = _utils.get_message_id(
                _utils.get_user_message_payload(
                   from_client_message=message
                )
            )
        except:
            raise exceptions.NotCorrectChatMessageFormat(message)

        await messages.async_delete_message(message_id=message_id)

        return message
