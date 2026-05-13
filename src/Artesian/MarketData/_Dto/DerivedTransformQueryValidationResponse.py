from dataclasses import dataclass
from typing import Optional
from .TimeSerieData import TimeSerieData


@dataclass
class Error:
    """
    Class Represents an error in the derived transform query validation response.
    Attributes:
        message: The Error message when the query validation is invalid

    """

    message: Optional[str] = None


@dataclass
class DerivedTransformQueryValidationResponse:
    """
    Class Represents the response of a derived transform query validation.
    Attributes:
        data: The time series data used for the query validation
        transform: The transform query string to be validated

    """

    data: TimeSerieData
    valid: bool
    error: Optional[Error] = None
