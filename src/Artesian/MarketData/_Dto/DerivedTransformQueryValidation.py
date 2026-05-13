from dataclasses import dataclass
from typing import Optional
from .TimeSerieData import TimeSerieData


@dataclass
class DerivedTransformQueryValidation:
    """
    Class Derived transform query validation.

    Attributes:
        data: The time series data used for the query validation
        transform: The transform query string to be validated

    """

    data: TimeSerieData
    transform: Optional[str] = None
