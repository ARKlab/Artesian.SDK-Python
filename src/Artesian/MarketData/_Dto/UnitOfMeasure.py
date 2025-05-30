from dataclasses import dataclass


@dataclass
class UnitOfMeasure:
    """
    Class for the UnitOfMeasure.

    Attributes:
        value: the value of the unit of measure for the values of timeseries
               (actual and versioned)

    """

    value: str
