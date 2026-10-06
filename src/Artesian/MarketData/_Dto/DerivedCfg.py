from dataclasses import dataclass

from .._Enum import DerivedAlgorithm


@dataclass
class DerivedCfg:
    """
    Class for the Derived Configuration.

    Attributes:
        derivedAlgorithm: the derived configuration algorithm (MUV, Coalesce, Sum, Transform)
        version: the derived configuration version
        orderedReferencedMarketDataIds: the ordered reference MarketData Ids
        used in the computation

    """

    derivedAlgorithm: DerivedAlgorithm
    version: int
    orderedReferencedMarketDataIds: list[int] | None
    transform: str | None = None
