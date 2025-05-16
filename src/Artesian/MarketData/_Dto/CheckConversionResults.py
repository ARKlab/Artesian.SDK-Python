from dataclasses import dataclass
from typing import List


@dataclass
class CheckConversionResults:
    """
    Class for the CheckConversionResults.

    Attributes:
        targetUnitOfMeasure: the target UnitOfMeasure
        convertibleInputUnitOfMeasure: the list of convertible input UnitOfMeasure
        notConvertibleInputUnitOfMeasure: the list of not convertible input
                                          UnitOfMeasure
    """

    targetUnitOfMeasure: str
    convertibleInputUnitOfMeasure: List[str]
    notConvertibleInputUnitOfMeasure: List[str]
