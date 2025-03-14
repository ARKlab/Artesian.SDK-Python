from dataclasses import dataclass
from typing import List, Optional
from Artesian.MarketData._Enum import DerivedAlgorithm


@dataclass
class DerivedCfg:
    """
    Class for the Derived Configuration.

    Attributes:
        derivedAlgorithm: the derived configuration algorithm (MUV, Coalesce, Sum)
        version: the derived configuration version 
        orderedReferencedMarketDataIds: the ordered reference MarketData Ids
        used in the computation

    """

    derivedAlgorithm: DerivedAlgorithm
    version: int
    orderedReferencedMarketDataIds: Optional[List[int]]
