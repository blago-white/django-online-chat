__all__ = [
    "get_user_message_payload",
    "get_message_data",
    "get_message_id"
]


def get_user_message_payload(from_client_message: dict) -> dict:
    return from_client_message.get("payload")


def get_message_data(payload: dict) -> tuple[int, str]:
    return int(payload["userid"]), payload["message"]


def get_message_id(payload: dict) -> tuple[int, str]:
    return int(payload["message_id"])
