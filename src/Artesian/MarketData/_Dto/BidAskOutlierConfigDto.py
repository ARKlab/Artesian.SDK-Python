from dataclasses import dataclass, field

from .._Enum.BidAskDataQualityField import BidAskDataQualityField
from .._Enum.MarketDataType import MarketDataType
from .OutlierConfigDto import OutlierConfigDto


@dataclass
class BidAskOutlierConfigDto(OutlierConfigDto):
    products: list[str] | None = None
    fieldsToBeValidated: list[BidAskDataQualityField] = field(kw_only=True)
    marketDataType: MarketDataType = field(default=MarketDataType.BidAsk, kw_only=True)
