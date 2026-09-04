from enum import Enum


class AlertType(Enum):
    """Determines when a quality notification alert is fired."""

    OnEvent = 0
    Scheduled = 1
