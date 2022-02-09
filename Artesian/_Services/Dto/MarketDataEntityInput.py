from dataclasses import dataclass, field
from typing import Optional
from .ArtesianTags import ArtesianTags
from ..Enum import MarketDataType
from ..Enum import AggregationRule
from ..Enum import Granularity

@dataclass
class MarketDataEntityInput:
    """ 
        Class for the Market Data Entity Input. 

        Attributes:
            providerName: the provider name for the market data entity input
            marketDataName: the market data name for the market data entity input
            originalGranularity: the original granularity for the market data entity input
            type: the market data type for the market data entity input
            originalTimezone: the original timezone for the market data entity input
            aggregationRule: the aggregation rule for the market data entity input
            tags: the Artesian Tags for the market data entity input
            providerDescription: the provider description for the market data entity input
            transformID: the time transform ID for the market data entity input
            marketDataId: the market data ID for the market data entity input
            eTag: the market data Etag for the market data entity input

    """  
    providerName: str
    marketDataName: str
    originalGranularity: Granularity
    type: MarketDataType
    originalTimezone: str
    aggregationRule: AggregationRule = AggregationRule.Undefined
    # the default_factory is needed otherwise the 'jsons' package do not hook into custom deserialize when using default values. \_-_/
    tags: Optional[ArtesianTags] = field(default_factory=lambda: None)
    providerDescription: str = None
    transformID: int = None
    marketDataId: int = 0
    eTag: str = None
    