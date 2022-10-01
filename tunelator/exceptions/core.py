from django.utils.translation import gettext_lazy as _

class UserNotFoundError(Exception):
    def __init__(self, search_fields: dict) -> None:
        self.search_fields = search_fields
        super().__init__()

    def __str__(self) -> str:
        return _("User with search fields %s was not found") % self.search_fields

class MailUserNotSentError(Exception):
    def __init__(self) -> None:
        super().__init__(_("No mail user id was sent"))

class MailUserNotFoundError(Exception):
    def __init__(self, search_fields: dict) -> None:
        self.search_fields = search_fields
        super().__init__()

    def __str__(self) -> str:
        return _("Mail user with search fields %s was not found") % self.search_fields

class InvalidMailUserIntegrationDataError(Exception):
    def __init__(self, data: str) -> None:
        self.data = data
        self.message = _("Invalid Mail User Integration Data")
        super().__init__(self.message)

    def __str__(self) -> str:
        return "%s: %s" % (self.message, self.data)

class ReceivedMailNotFound(Exception):
    def __init__(self, search_fields: dict) -> None:
        self.search_fields = search_fields
        super().__init__()

    def __str__(self) -> str:
        return _("Received mail with search fields %s was not found") % self.search_fields

class FileReadError(Exception):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()

    def __str__(self) -> str:
        return _("Error reading file: %s") % self.path

class FreePlanNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__(_("Free plan not found for attribution"))
