from .._Enum import DerivedAlgorithm
from .DerivedCfgBase import DerivedCfgBase


class DerivedCfgCoalesce(DerivedCfgBase):
    """
    Derived Cfg Coalesce
    """

    derivedAlgorithm = DerivedAlgorithm.Coalesce

    orderedReferencedMarketDataIds = []
