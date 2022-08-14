class UserNotFoundError(Exception):
    def __init__(self, search_fields: dict) -> None:
        self.search_fields = search_fields
        super().__init__()

    def __str__(self) -> str:
        return "User with search fields %s was not found" % self.search_fields
