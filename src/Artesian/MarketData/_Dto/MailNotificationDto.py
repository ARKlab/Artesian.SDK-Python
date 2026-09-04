from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MailNotificationDto:
    """
    Email notification configuration for quality alerts.

    Attributes:
        recipients: The array of recipient email addresses to which the quality alert notification will be sent
    """

    recipients: Optional[List[str]] = None
