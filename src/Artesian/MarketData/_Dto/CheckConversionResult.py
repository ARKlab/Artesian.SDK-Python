from dataclasses import dataclass


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
    convertibleInputUnitsOfMeasure: list[str]
    notConvertibleInputUnitsOfMeasure: list[str]
