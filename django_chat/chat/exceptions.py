class NotCorrectChatMessageFormat(BaseException):
    def __repr__(self):
        return "Сhat message must be a dictionary and contain a message (string) and a user ID (integer)"
