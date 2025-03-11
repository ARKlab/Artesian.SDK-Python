from dataclasses import dataclass
from typing import Dict, List, Optional

from Artesian.MarketData._Dto.DerivedCfg import DerivedCfg
from .._Enum import MarketDataType
from .._Enum import AggregationRule
from .._Enum import Granularity


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
        derivedCfg: the derived configuration for the market data entity input

    """

    providerName: str
    marketDataName: str
    originalGranularity: Granularity
    type: MarketDataType
    originalTimezone: str
    derivedCfg: Optional[DerivedCfg] = None
    aggregationRule: AggregationRule = AggregationRule.Undefined
    tags: Optional[Dict[str, List[str]]] = None
    providerDescription: Optional[str] = None
    transformID: Optional[int] = None
    marketDataId: int = 0
    eTag: Optional[str] = None
