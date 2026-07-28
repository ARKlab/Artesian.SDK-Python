from dataclasses import dataclass
from typing import Dict, List, Optional

from .DerivedCfg import DerivedCfg
from .UnitOfMeasure import UnitOfMeasure
from .._Enum.DerivedAlgorithm import DerivedAlgorithm
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
    unitOfMeasure: Optional[UnitOfMeasure] = None
    derivedCfg: Optional[DerivedCfg] = None
    aggregationRule: AggregationRule = AggregationRule.Undefined
    tags: Optional[Dict[str, List[str]]] = None
    providerDescription: Optional[str] = None
    transformID: Optional[int] = None
    marketDataId: int = 0
    eTag: Optional[str] = None

    def _validateDerivedCfg(
            self: "MarketDataEntityInput") -> None:
        if (
            self.derivedCfg is not None
            and self.derivedCfg.derivedAlgorithm == DerivedAlgorithm.MUV
            and self.derivedCfg.orderedReferencedMarketDataIds is not None
        ):
            raise Exception(
                "DerivedCfg with MUV algorithm cannot have "
                "orderedReferencedMarketDataIds"
            )

        if (
            self.derivedCfg is not None
            and self.derivedCfg.derivedAlgorithm is not DerivedAlgorithm.MUV
            and self.derivedCfg.orderedReferencedMarketDataIds is None
        ):
            raise Exception(
                f"DerivedCfg with {self.derivedCfg.derivedAlgorithm} algorithm "
                "must have orderedReferencedMarketDataIds valorized or empty []"
            )

        if (
            self.derivedCfg is not None
            and self.derivedCfg.derivedAlgorithm in {
                DerivedAlgorithm.Coalesce,
                DerivedAlgorithm.Sum
                }
            and self.type is not MarketDataType.ActualTimeSerie
        ):
            raise Exception(
                f"DerivedCfg with {self.derivedCfg.derivedAlgorithm} algorithm "
                "must be set to MarketData of type Actual only."
            )

        if (
            self.derivedCfg is not None
            and self.derivedCfg.derivedAlgorithm is DerivedAlgorithm.MUV
            and self.type is not MarketDataType.VersionedTimeSerie
        ):
            raise Exception(
                f"DerivedCfg with {self.derivedCfg.derivedAlgorithm} algorithm "
                "must be set to MarketData of type Versioned only."
            )
