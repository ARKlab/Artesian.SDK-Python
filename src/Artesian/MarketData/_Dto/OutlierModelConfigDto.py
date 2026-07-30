from dataclasses import dataclass

from .._Enum.OutlierModel import OutlierModel
from .DataQualityRuleConfigDto import DataQualityRuleConfigDto


from dataclasses import dataclass, field

from .._Enum.OutlierModel import OutlierModel
from .._Enum.RuleType import RuleType
from .DataQualityRuleConfigDto import DataQualityRuleConfigDto


@dataclass
class OutlierModelConfigDto(DataQualityRuleConfigDto):
    """
    Base configuration for outlier detection rules.
    """

    type: RuleType = field(init=False, default=RuleType.Outlier)

    @property
    def model(self: "OutlierModelConfigDto") -> OutlierModel:
        raise NotImplementedError(
            "OutlierModelConfigDto.model must be implemented by subclasses"
        )
