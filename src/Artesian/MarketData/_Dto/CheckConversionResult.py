from dataclasses import dataclass
from typing import List


@dataclass
class CheckConversionResult:
    """
    Class for the CheckConversionResult.

    Attributes:
        targetUnitOfMeasure: the target UnitOfMeasure
        convertibleInputUnitsOfMeasure: the list of convertible input UnitOfMeasure
        notConvertibleInputUnitsOfMeasure: the list of not convertible input
                                          UnitOfMeasure
    """

    targetUnitOfMeasure: str
    convertibleInputUnitsOfMeasure: List[str]
    notConvertibleInputUnitsOfMeasure: List[str]
