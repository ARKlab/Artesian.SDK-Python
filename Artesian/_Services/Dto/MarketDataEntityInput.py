from dataclasses import field
from ArtesianTags import ArtesianTags
from Enum import MarketDataType
from Enum import AggregationRule
from Enum import Granularity


class MarketDataEntityInput:
    providerName: str
    marketDataName: str
    originalGranularity: Granularity
    type: MarketDataType
    originalTimezone: str
    aggregationRule: AggregationRule = AggregationRule.Undefined
    # the default_factory is needed otherwise the 'jsons' package do not hook into custom deserialize when using default values. \_-_/
    tags: ArtesianTags = field(default_factory=lambda: None)
    providerDescription: str = None
    transformID: int = None
    marketDataId: int = 0
    eTag: str = None