from dataclasses import dataclass, field

from .._Enum.RuleType import RuleType
from .DataQualityRuleConfigDto import DataQualityRuleConfigDto
from .OutlierModelConfigDto import OutlierModelConfigDto


@dataclass
class OutlierConfigDto(DataQualityRuleConfigDto):
    """
    Configuration for Outlier detection rules.

    Contains a polymorphic model that defines the specific statistical
    approach and parameters used to identify anomalous data points.
    """

    model: OutlierModelConfigDto
    type: RuleType = field(init=False, default=RuleType.Outlier)
