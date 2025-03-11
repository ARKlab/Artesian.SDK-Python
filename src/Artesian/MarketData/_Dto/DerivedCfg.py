from dataclasses import dataclass
from typing import List, Optional
from Artesian.MarketData._Enum import DerivedAlgorithm


@dataclass
class DerivedCfg:
    derivedAlgorithm: DerivedAlgorithm
    version: int
    orderedReferencedMarketDataIds: Optional[List[int]]
