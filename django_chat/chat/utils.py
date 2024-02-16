def get_websocket_response_dict(message_from_client: dict,
                                saved_dict: dict) -> dict:
    return {
        "id": saved_dict["id"],
        "text": "text"
    }
