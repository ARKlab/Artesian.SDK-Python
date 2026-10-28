from dataclasses import dataclass, field

from .._Enum.MarketDataType import MarketDataType
from .._Enum.MasDataQualityField import MasDataQualityField
from .CompletenessAndFreshnessConfigDto import CompletenessAndFreshnessConfigDto


@dataclass
class MasCompletenessAndFreshnessConfigDto(CompletenessAndFreshnessConfigDto):
    products: list[str]
    fieldsToBeValidated: list[MasDataQualityField] = field(kw_only=True)
    marketDataType: MarketDataType = field(
        default=MarketDataType.MarketAssessment,
        kw_only=True,
    )
