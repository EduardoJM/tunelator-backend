class FreePlanNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Free plan not found for attribution")
