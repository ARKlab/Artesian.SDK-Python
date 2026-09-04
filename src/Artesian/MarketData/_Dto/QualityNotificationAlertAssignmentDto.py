from dataclasses import dataclass
from typing import Optional

from .MarketDataEntityOutputEnriched import MarketDataEntityOutputEnriched
from .QualityNotificationAlertDto import QualityNotificationAlertDtoOutput


@dataclass
class QualityNotificationAlertAssignmentDtoInput:
    """
    Write model for creating or updating an alert / Market Data assignment.

    Contains only the foreign-key identifiers and concurrency token.

    Attributes:
        id: The unique identifier of the assignment, assigned by the server on
            creation.
        alertId: The identifier of the notification alert that monitors the
            Market Data.
        marketDataId: The identifier of the Market Data entity monitored by
            the alert.
        eTag: The entity tag for optimistic concurrency control.
    """

    id: int = 0
    alertId: int = 0
    marketDataId: int = 0
    eTag: Optional[str] = None


@dataclass
class QualityNotificationAlertAssignmentDtoOutput(
    QualityNotificationAlertAssignmentDtoInput
):
    """
    Read model returned by GET operations.

    Extends the input model with expanded navigation properties for the
    associated Market Data and Alert.

    Attributes:
        marketData: The enriched Market Data entity associated with this
            assignment.
        alert: The notification alert definition associated with this
            assignment.
    """

    marketData: Optional[MarketDataEntityOutputEnriched] = None
    alert: Optional[QualityNotificationAlertDtoOutput] = None


QualityNotificationAlertAssignmentInput = QualityNotificationAlertAssignmentDtoInput
QualityNotificationAlertAssignmentOutput = QualityNotificationAlertAssignmentDtoOutput
