from dataclasses import dataclass, field

from .._Enum.MarketDataType import MarketDataType
from .._Enum.MasDataQualityField import MasDataQualityField
from .OutlierConfigDto import OutlierConfigDto


@dataclass
class MasOutlierConfigDto(OutlierConfigDto):
    products: list[str] | None = None
    fieldsToBeValidated: list[MasDataQualityField] = field(kw_only=True)
    marketDataType: MarketDataType = field(default=MarketDataType.MarketAssessment, kw_only=True)
