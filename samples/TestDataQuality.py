import Artesian
from Artesian.MarketData._Dto.ActualCompletenessAndFreshnessConfigDto import (
    ActualCompletenessAndFreshnessConfigDto,
)
from Artesian.MarketData._Dto.CronScheduleDefinitionDto import CronScheduleDefinitionDto
from Artesian.MarketData._Dto.DataQualityRuleDtoInput import DataQualityRuleDtoInput
from Artesian.MarketData._Dto.RecordValidationConfigDto import RecordValidationConfigDto
from Artesian.MarketData._Dto.ScheduleConfigDto import ScheduleConfigDto
from Artesian.MarketData._Enum.MarketDataTypeV2 import MarketDataTypeV2
from Artesian.MarketData._Enum.RuleType import RuleType

# Run only manually with proper Artesian URI and ApiKey set.
cfg = Artesian.ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = Artesian.MarketData.MarketDataService(cfg)

ruleCreated = None

try:
    completenessCfg = ActualCompletenessAndFreshnessConfigDto(
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
    )

    # Register rule
    rulePayload = DataQualityRuleDtoInput(
        id=0,
        name="TestRule",
        type=RuleType.CompletenessAndFreshness,
        configuration=completenessCfg,
        version=0,
    )
    ruleCreated = mkdservice.registerDataQualityRule(rulePayload)

    # Read rule
    readDataQualityRule = mkdservice.readDataQualityRuleById(ruleCreated.id)
    assert readDataQualityRule is not None
    assert readDataQualityRule.id == ruleCreated.id

    # Update rule
    updatedCompletenessCfg = ActualCompletenessAndFreshnessConfigDto(
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
    )

    updatePayload = DataQualityRuleDtoInput(
        id=ruleCreated.id,
        name="TestRuleUpdated",
        type=RuleType.CompletenessAndFreshness,
        configuration=updatedCompletenessCfg,
        version=readDataQualityRule.version,
        eTag=readDataQualityRule.eTag,
    )

    mkdservice.updateDataQualityRule(ruleCreated.id, updatePayload)

    readDataQualityRule = mkdservice.readDataQualityRuleById(ruleCreated.id)
    assert readDataQualityRule is not None
    assert readDataQualityRule.name == "TestRuleUpdated"

    # Delete rule
    mkdservice.deleteDataQualityRule(ruleCreated.id)

    readDataQualityRule = mkdservice.readDataQualityRuleById(ruleCreated.id)
    assert readDataQualityRule is None

    print("Test completed")
finally:
    # Best-effort cleanup in case the test fails in the middle.
    if ruleCreated is not None:
        try:
            mkdservice.deleteDataQualityRule(ruleCreated.id)
        except Exception as ex:
            print(f"Best-effort cleanup failed for rule id {ruleCreated.id}: {ex}")
