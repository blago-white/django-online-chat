from channels.generic.websocket import AsyncWebsocketConsumer

from .services import messages, consumers_services


class ChatConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data=None, bytes_data=None):
        try:
            userid, message = consumers_services.get_user_message_payload(text_data=text_data)
            await messages.async_save_message(from_user_id=userid, text=message)
        except:
            pass
