from dataclasses import dataclass


@dataclass
class MailNotificationDto:
    """
    Email notification configuration for quality alerts.

    Attributes:
        recipients: The array of recipient email addresses to which the quality alert notification will be sent
    """

    recipients: list[str] | None = None
