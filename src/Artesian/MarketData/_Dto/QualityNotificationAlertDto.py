from dataclasses import dataclass
from typing import List, Optional

from .MailNotificationDto import MailNotificationDto
from .TriggerConfigDto import TriggerConfigDto


@dataclass
class QualityNotificationAlertDtoInput:
    """
    Write model for creating or updating a notification alert.

    Attributes:
        name: a human-readable name for this alert (e.g., "Weather station daily digest")
        triggerConfig: the trigger configuration determining when notifications are sent
        id: the unique identifier of this notification alert, assigned by the server on creation
        mailNotifications: the configured email notification recipients
        eTag: the entity tag for optimistic concurrency control
        version: monotonically increasing version counter, incremented on each update.
                 used as a guard for deferred alert schedule messages
    """

    name: str
    triggerConfig: TriggerConfigDto
    id: int = 0
    mailNotifications: Optional[List[MailNotificationDto]] = None
    eTag: Optional[str] = None
    version: int = 0


@dataclass
class QualityNotificationAlertDtoOutput(QualityNotificationAlertDtoInput):
    """Read model returned by GET operations."""
