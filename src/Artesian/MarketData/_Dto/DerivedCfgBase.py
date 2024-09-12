from abc import ABC
from .._Enum import DerivedAlgorithm


class DerivedCfgBase(ABC):
    """
    Class for Derived Curve Configuration
    """

    version: int
    derivedAlgorithm: DerivedAlgorithm
