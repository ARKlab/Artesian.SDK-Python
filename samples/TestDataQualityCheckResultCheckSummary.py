import time
from datetime import datetime
from uuid import uuid4

import Artesian
from Artesian.Granularity import Granularity
from Artesian.MarketData._Dto.ActualCompletenessAndFreshnessConfigDto import (
    ActualCompletenessAndFreshnessConfigDto,
)
from Artesian.MarketData._Dto.CronScheduleDefinitionDto import CronScheduleDefinitionDto
from Artesian.MarketData._Dto.DataQualityRuleDtoInput import DataQualityRuleDtoInput
from Artesian.MarketData._Dto.MarketDataEntityInput import MarketDataEntityInput
from Artesian.MarketData._Dto.MarketDataQualityRuleAssignmentDto import (
    MarketDataQualityRuleAssignmentDtoInput,
)
from Artesian.MarketData._Dto.RecordValidationConfigDto import RecordValidationConfigDto
from Artesian.MarketData._Dto.ScheduleConfigDto import ScheduleConfigDto
from Artesian.MarketData._Enum.AggregationRule import AggregationRule
from Artesian.MarketData._Enum.MarketDataTypeV2 import MarketDataTypeV2
from Artesian.MarketData._Enum.RuleType import RuleType

# Run only manually with proper Artesian URI and ApiKey set.
cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
marketDataService = Artesian.MarketData.MarketDataService(cfg)

marketDataId = None
ruleId = None
assignmentId = None

try:
    # Step 1: Create a Daily Actual TimeSerie named TsCheckSummaryQuery from Provider DqCheckResult
    provider_name = "DqCheckResult"
    market_data_name = "TsCheckSummaryQuery_" + str(uuid4())

    market_data_input = MarketDataEntityInput(
        providerName=provider_name,
        marketDataName=market_data_name,
        type=MarketDataTypeV2.ActualTimeSerie,
        originalGranularity=Granularity.Day,
        originalTimezone="UTC",
        aggregationRule=AggregationRule.Undefined,
    )

    registered = marketDataService.readMarketDataRegistryByName(provider_name, market_data_name)
    if registered is None:
        registered = marketDataService.registerMarketData(market_data_input)

    marketDataId = registered.marketDataId

    # Step 2: Write values with gaps (2025-01-01, 2025-01-03, 2025-01-05)
    mkt_id = Artesian.MarketData.MarketDataIdentifier(provider_name, market_data_name)
    data = Artesian.MarketData.UpsertData(
        mkt_id,
        "UTC",
        rows={
            datetime(2025, 1, 1): 10.0,
            datetime(2025, 1, 3): 10.0,
            datetime(2025, 1, 5): 10.0,
        },
    )
    marketDataService.upsertData(data)

    # Step 3: Create a data quality rule
    rule_payload = DataQualityRuleDtoInput(
        name="TsSummaryRule_" + str(uuid4()),
        type=RuleType.CompletenessAndFreshness,
        configuration=ActualCompletenessAndFreshnessConfigDto(
            marketDataType=MarketDataTypeV2.ActualTimeSerie,
            scheduleConfig=ScheduleConfigDto(
                scheduleDefinition=CronScheduleDefinitionDto(
                    cronExpression="0 0 * * *",
                    timeZone="UTC",
                ),
                maxDelay="PT1H",
            ),
            recordValidationConfig=RecordValidationConfigDto(
                recordRangeFrom="P0D",
                recordRangeTo="P1D",
            ),
        ),
        version=0,
    )

    rule_created = marketDataService.registerDataQualityRule(rule_payload)
    ruleId = rule_created.id
    assert rule_created is not None
    assert rule_created.name == rule_payload.name

    # Step 4: Create assignment with initializationLookbackPeriod P13D
    assignment_payload = MarketDataQualityRuleAssignmentDtoInput(
        marketDataId=marketDataId,
        dataQualityRuleId=rule_created.id,
    )

    assignment_created = marketDataService.registerDataQualityRuleAssignment(
        assignment_payload,
        initializationLookbackPeriod="P13D",
    )
    assignmentId = assignment_created.id
    assert assignment_created is not None
    assert assignment_created.dataQualityRuleId == assignment_payload.dataQualityRuleId

    # Step 5: Wait for deferred execution to complete
    time.sleep(5)

    # Step 6: Query the check result check summary
    check_summary_result = marketDataService.getDataQualityCheckResultCheckSummary(
        page=1,
        pageSize=100,
        assignmentIds=[assignment_created.id],
    )

    # Step 7: Verify the results
    assert check_summary_result is not None
    assert check_summary_result.data is not None

    print("DataQualityCheckResultCheckSummary test completed")

finally:
    # Best-effort cleanup in case the test fails in the middle.
    if assignmentId is not None:
        try:
            marketDataService.deleteDataQualityRuleAssignment(assignmentId)
        except Exception as ex:
            print(f"Best-effort cleanup failed for assignment id {assignmentId}: {ex}")

    if ruleId is not None:
        try:
            marketDataService.deleteDataQualityRule(ruleId)
        except Exception as ex:
            print(f"Best-effort cleanup failed for rule id {ruleId}: {ex}")

    if marketDataId is not None:
        try:
            marketDataService.deleteMarketData(marketDataId)
        except Exception as ex:
            print(f"Best-effort cleanup failed for market data id {marketDataId}: {ex}")
