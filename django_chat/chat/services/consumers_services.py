import json


def get_user_message_payload(text_data: str) -> tuple[int, str]:
    from_client_message = json.loads(text_data)
    return int(from_client_message["userid"]), from_client_message["message"]
