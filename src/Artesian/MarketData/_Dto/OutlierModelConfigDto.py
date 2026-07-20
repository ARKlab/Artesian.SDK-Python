from dataclasses import dataclass

from .._Enum.OutlierModel import OutlierModel
from .DataQualityRuleConfigDto import DataQualityRuleConfigDto


@dataclass
class OutlierModelConfigDto(DataQualityRuleConfigDto):
    """
    Base configuration for outlier detection rules.
    """

    @property
    def model(self: "OutlierModelConfigDto") -> OutlierModel:
        raise NotImplementedError(
            "OutlierModelConfigDto.model must be implemented by subclasses"
        )
