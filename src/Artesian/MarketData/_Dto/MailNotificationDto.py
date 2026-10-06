from dataclasses import dataclass
from typing import Optional


@dataclass
class MailNotificationDto:
    """
    Email notification configuration for quality alerts.

    Attributes:
        recipients: The array of recipient email addresses to which the quality alert notification will be sent
    """

    recipients: Optional[list[str]] = None
