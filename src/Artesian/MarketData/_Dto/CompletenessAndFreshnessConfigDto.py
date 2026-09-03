from dataclasses import dataclass, field

from .._Enum.MarketDataType import MarketDataType
from .._Enum.RuleType import RuleType
from .DataQualityRuleConfigDto import DataQualityRuleConfigDto
from .RecordValidationConfigDto import RecordValidationConfigDto
from .ScheduleConfigDto import ScheduleConfigDto


@dataclass
class CompletenessAndFreshnessConfigDto(DataQualityRuleConfigDto):
    """
    Abstract configuration for Completeness and Freshness rules.

    Validates that expected data records are present within the defined
    time window and arrive within an acceptable delay.
    """

    marketDataType: MarketDataType
    scheduleConfig: ScheduleConfigDto
    recordValidationConfig: RecordValidationConfigDto
    type: RuleType = field(init=False, default=RuleType.CompletenessAndFreshness)
