from uuid import uuid4

import Artesian
from Artesian.Granularity import Granularity
from Artesian.MarketData._Dto.MailNotificationDto import MailNotificationDto
from Artesian.MarketData._Dto.MarketDataEntityInput import MarketDataEntityInput
from Artesian.MarketData._Dto.QualityNotificationAlertAssignmentDto import (
    QualityNotificationAlertAssignmentDtoInput,
)
from Artesian.MarketData._Dto.QualityNotificationAlertDto import (
    QualityNotificationAlertDtoInput,
)
from Artesian.MarketData import OnEventTriggerConfigDto
from Artesian.MarketData._Enum.AggregationRule import AggregationRule
from Artesian.MarketData._Enum.MarketDataType import MarketDataType

# Run only manually with proper Artesian URI and ApiKey set.
cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
marketDataService = Artesian.MarketData.MarketDataService(cfg)


alertId = None
marketDataId = None
assignmentId = None

try:
    providerName = "DataQualityNotificationAlertSample"
    marketDataName = str(uuid4())
    marketDataPayload = MarketDataEntityInput(
        providerName=providerName,
        marketDataName=marketDataName,
        type=MarketDataType.ActualTimeSerie,
        originalGranularity=Granularity.Hour,
        originalTimezone="UTC",
        aggregationRule=AggregationRule.Undefined,
    )
    marketData = marketDataService.registerMarketData(marketDataPayload)
    marketDataId = marketData.marketDataId
    assert marketDataId > 0

    alertPayload = QualityNotificationAlertDtoInput(
        name="Data quality notification alert assignment sample",
        triggerConfig=OnEventTriggerConfigDto(),
        mailNotifications=[
            MailNotificationDto(recipients=["quality-alerts@example.com"])
        ],
    )
    alert = marketDataService.registerQualityNotificationAlert(alertPayload)
    alertId = alert.id
    assert alertId > 0

    assignmentPayload = QualityNotificationAlertAssignmentDtoInput(
        alertId=alertId,
        marketDataId=marketDataId,
    )

    assignmentCreated = marketDataService.registerQualityNotificationAlertAssignment(
        assignmentPayload
    )
    assignmentId = assignmentCreated.id
    assert assignmentId > 0

    assignment = marketDataService.readQualityNotificationAlertAssignmentById(
        assignmentId
    )
    assert assignment is not None
    assert assignment.id == assignmentId
    assert assignment.alertId == alertId
    assert assignment.marketDataId == marketDataId

    assignments = marketDataService.readQualityNotificationAlertAssignments(
        page=1,
        pageSize=10,
        alertId=alertId,
        marketDataId=marketDataId,
        sort=["Id asc"],
    )
    assert assignments is not None
    assert any(item.id == assignmentId for item in assignments.data)

    marketDataService.deleteQualityNotificationAlertAssignment(assignmentId)
    assignmentId = None

    marketDataService.deleteQualityNotificationAlert(alertId)
    alertId = None

    marketDataService.deleteMarketData(marketDataId)
    marketDataId = None

    print("Data quality notification alert assignment sample completed")
finally:
    if assignmentId is not None:
        try:
            marketDataService.deleteQualityNotificationAlertAssignment(assignmentId)
        except Exception as ex:
            print(
                f"Best-effort cleanup failed for assignment id {assignmentId}: {ex}"
            )

    if alertId is not None:
        try:
            marketDataService.deleteQualityNotificationAlert(alertId)
        except Exception as ex:
            print(f"Best-effort cleanup failed for alert id {alertId}: {ex}")

    if marketDataId is not None:
        try:
            marketDataService.deleteMarketData(marketDataId)
        except Exception as ex:
            print(f"Best-effort cleanup failed for market data id {marketDataId}: {ex}")
