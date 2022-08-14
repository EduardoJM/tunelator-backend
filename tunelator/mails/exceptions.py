class MailUserNotSentError(Exception):
    def __init__(self) -> None:
        super().__init__("No mail user id was sent")

class MailUserNotFoundError(Exception):
    def __init__(self, search_fields: dict) -> None:
        self.search_fields = search_fields
        super().__init__()

    def __str__(self) -> str:
        return "Mail user with search fields %s was not found" % self.search_fields

class InvalidMailUserIntegrationDataError(Exception):
    def __init__(self, data: str) -> None:
        self.data = data
        self.message = "Invalid Mail User Integration Data"
        super().__init__(self.message)

    def __str__(self) -> str:
        return "%s: %s" % (self.message, self.data)

class ReceivedMailNotFound(Exception):
    def __init__(self, search_fields: dict) -> None:
        self.search_fields = search_fields
        super().__init__()

    def __str__(self) -> str:
        return "Received mail with search fields %s was not found" % self.search_fields

class FileReadError(Exception):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()

    def __str__(self) -> str:
        return "Error reading file: %s" % self.path
