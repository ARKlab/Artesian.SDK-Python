from dataclasses import dataclass, field

from .._Enum.BidAskDataQualityField import BidAskDataQualityField
from .._Enum.MarketDataType import MarketDataType
from .CompletenessAndFreshnessConfigDto import CompletenessAndFreshnessConfigDto


@dataclass
class BidAskCompletenessAndFreshnessConfigDto(CompletenessAndFreshnessConfigDto):
    products: list[str]
    fieldsToBeValidated: list[BidAskDataQualityField] = field(kw_only=True)
    marketDataType: MarketDataType = field(default=MarketDataType.BidAsk, kw_only=True)
