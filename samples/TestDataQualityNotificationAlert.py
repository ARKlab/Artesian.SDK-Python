import Artesian
from Artesian.MarketData._Dto.MailNotificationDto import MailNotificationDto
from Artesian.MarketData._Dto.QualityNotificationAlertDto import (
    QualityNotificationAlertDtoInput,
)
from Artesian.MarketData import OnEventTriggerConfigDto

# Run only manually with proper Artesian URI and ApiKey set.
cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
marketDataService = Artesian.MarketData.MarketDataService(cfg)


alertId = None

try:
    alertPayload = QualityNotificationAlertDtoInput(
        name="Data quality notification alert sample",
        triggerConfig=OnEventTriggerConfigDto(),
        mailNotifications=[
            MailNotificationDto(recipients=["quality-alerts@example.com"])
        ],
    )

    alertCreated = marketDataService.registerQualityNotificationAlert(alertPayload)
    alertId = alertCreated.id
    assert alertId > 0

    readAlert = marketDataService.readQualityNotificationAlertById(alertId)
    assert readAlert is not None
    assert readAlert.id == alertId

    alerts = marketDataService.readQualityNotificationAlerts(page=1, pageSize=10)
    assert alerts is not None

    marketDataService.deleteQualityNotificationAlert(alertId)
    alertId = None

    print("Data quality notification alert sample completed")
finally:
    if alertId is not None:
        try:
            marketDataService.deleteQualityNotificationAlert(alertId)
        except Exception as ex:
            print(f"Best-effort cleanup failed for alert id {alertId}: {ex}")
