from dataclasses import dataclass
import datetime
from typing import Optional

from .DerivedCfg import DerivedCfg
from .MarketDataEntityInput import MarketDataEntityInput


@dataclass
class MarketDataEntityOutput(MarketDataEntityInput):
    """
    Class for the Market Data Entity Output.

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
        lastUpdated: the last time the metadata has been updated
        dataLastWritedAt: the last time the data has been written at
        dataRangeStart: start date of range for this curve
        dataRangeEnd: end date of range for this curve
        created: the time the market data has been created
    """

    lastUpdated: Optional[datetime.datetime] = None
    dataLastWritedAt: Optional[datetime.datetime] = None
    dataRangeStart: Optional[datetime.date] = None
    dataRangeEnd: Optional[datetime.date] = None
    created: Optional[datetime.datetime] = None
    # tranform: missing due to handling class hierarchies deserializations

    def _validateUpdateDerivedCfg(
            self: "MarketDataEntityOutput",
            derivedCfgUpdate: DerivedCfg) -> None:
        if self.derivedCfg is None:
            raise Exception(
                "DerivedCfg cannot be added to a MarketData that has not"
            )

        if self.derivedCfg.derivedAlgorithm != derivedCfgUpdate.derivedAlgorithm:
            raise Exception(
                "Derived Algorithm cannot be update"
            )
