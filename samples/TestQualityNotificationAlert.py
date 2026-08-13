from dataclasses import dataclass

import Artesian
from Artesian.MarketData._Dto.MailNotificationDto import MailNotificationDto
from Artesian.MarketData._Dto.QualityNotificationAlertDto import (
    QualityNotificationAlertDtoInput,
    QualityNotificationAlertDtoOutput,
)
from Artesian.MarketData._Dto.TriggerConfigDto import TriggerConfigDto
from Artesian.MarketData._Enum.AlertType import AlertType

# Run only manually with proper Artesian URI and ApiKey set.
cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
marketDataService = Artesian.MarketData.MarketDataService(cfg)


@dataclass
class OnEventTriggerConfig(TriggerConfigDto):
    """Minimal on-event trigger configuration used by this sample."""

    @property
    def type(self: "OnEventTriggerConfig") -> AlertType:
        return AlertType.OnEvent


# The Python serializer needs a concrete class for the abstract trigger payload.
QualityNotificationAlertDtoInput.__init__.__annotations__["triggerConfig"] = (
    OnEventTriggerConfig
)
QualityNotificationAlertDtoOutput.__init__.__annotations__["triggerConfig"] = (
    OnEventTriggerConfig
)

alertCreated = None

try:
    alertPayload = QualityNotificationAlertDtoInput(
        name="Weather station quality alert",
        triggerConfig=OnEventTriggerConfig(),
        mailNotifications=[
            MailNotificationDto(recipients=["quality-alerts@example.com"])
        ],
        version=0,
    )

    # Register alert.
    alertCreated = marketDataService.registerQualityNotificationAlert(alertPayload)
    assert alertCreated is not None
    assert alertCreated.id > 0

    # Read alert.
    readAlert = marketDataService.readQualityNotificationAlertById(alertCreated.id)
    assert readAlert is not None
    assert readAlert.id == alertCreated.id

    # Update alert using the server version and ETag.
    updatePayload = QualityNotificationAlertDtoInput(
        id=readAlert.id,
        name="Weather station quality alert updated",
        triggerConfig=OnEventTriggerConfig(),
        mailNotifications=readAlert.mailNotifications or [],
        version=readAlert.version,
        eTag=readAlert.eTag,
    )
    marketDataService.updateQualityNotificationAlert(alertCreated.id, updatePayload)

    readAlert = marketDataService.readQualityNotificationAlertById(alertCreated.id)
    assert readAlert is not None
    assert readAlert.name == "Weather station quality alert updated"

    # Read the paginated alert list.
    alerts = marketDataService.readQualityNotificationAlerts(
        page=1,
        pageSize=10,
        name="Weather station",
    )
    assert alerts is not None

    # Delete alert.
    marketDataService.deleteQualityNotificationAlert(alertCreated.id)

    readAlert = marketDataService.readQualityNotificationAlertById(alertCreated.id)
    assert readAlert is None

    print("Quality notification alert test completed")
finally:
    # Best-effort cleanup in case the test fails in the middle.
    if alertCreated is not None:
        try:
            marketDataService.deleteQualityNotificationAlert(alertCreated.id)
        except Exception as ex:
            print(
                f"Best-effort cleanup failed for alert id "
                f"{alertCreated.id}: {ex}"
            )
