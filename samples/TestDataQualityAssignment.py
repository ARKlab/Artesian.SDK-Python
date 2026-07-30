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
    # Register a market data entity to assign the rule to.
    provider_name = "SpecFlowDataQuality"
    market_data_name = str(uuid4())

    market_data_input = MarketDataEntityInput(
        providerName=provider_name,
        marketDataName=market_data_name,
        type=MarketDataTypeV2.ActualTimeSerie,
        originalGranularity=Granularity.Hour,
        originalTimezone="UTC",
        aggregationRule=AggregationRule.Undefined,
    )

    registered_market_data = marketDataService.readMarketDataRegistryByName(
        provider_name,
        market_data_name,
    )
    if registered_market_data is None:
        registered_market_data = marketDataService.registerMarketData(market_data_input)

    marketDataId = registered_market_data.marketDataId

    # Register rule.
    rule_payload = DataQualityRuleDtoInput(
        name="TestRule",
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
                recordRangeFrom="PT0S",
                recordRangeTo="PT1H",
            ),
        ),
        version=0,
    )

    rule_created = marketDataService.registerDataQualityRule(rule_payload)
    ruleId = rule_created.id

    read_data_quality_rule = marketDataService.readDataQualityRuleById(rule_created.id)
    assert read_data_quality_rule is not None
    assert read_data_quality_rule.id == rule_created.id

    # Assign rule to market data.
    assignment_payload = MarketDataQualityRuleAssignmentDtoInput(
        marketDataId=marketDataId,
        dataQualityRuleId=read_data_quality_rule.id,
    )

    assert assignment_payload.dataQualityRuleId == rule_created.id

    assignment_created = marketDataService.registerDataQualityRuleAssignment(
        assignment_payload
    )
    assignmentId = assignment_created.id

    data_quality_rule_assignment = marketDataService.readDataQualityRuleAssignmentById(
        assignment_created.id
    )
    assert data_quality_rule_assignment is not None
    assert data_quality_rule_assignment.id == assignment_created.id

    # Delete assignment.
    marketDataService.deleteDataQualityRuleAssignment(assignment_created.id)
    assignmentId = None

    data_quality_rule_assignment = marketDataService.readDataQualityRuleAssignmentById(
        assignment_created.id
    )
    assert data_quality_rule_assignment is None

    # Delete rule.
    marketDataService.deleteDataQualityRule(rule_created.id)
    ruleId = None

    read_data_quality_rule = marketDataService.readDataQualityRuleById(rule_created.id)
    assert read_data_quality_rule is None

    print("Data quality assignment test completed")
finally:
    # Best-effort cleanup in case the test fails in the middle.
    if assignmentId is not None:
        try:
            marketDataService.deleteDataQualityRuleAssignment(assignmentId)
        except Exception as ex:
            print(
                f"Best-effort cleanup failed for assignment id {assignmentId}: {ex}"
            )

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
