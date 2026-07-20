from dataclasses import dataclass

from .._Enum.OutlierModel import OutlierModel
from .OutlierModelConfigDto import OutlierModelConfigDto


@dataclass
class OutlierAbsoluteBoundConfigDto(OutlierModelConfigDto):
    """
    Outlier detection model using fixed absolute bounds.

    A data point is flagged as an outlier if its value falls below
    lowerBound or above upperBound.

    Attributes:
        upperBound: maximum acceptable value
        lowerBound: minimum acceptable value
    """

    upperBound: float
    lowerBound: float

    @property
    def model(self: "OutlierAbsoluteBoundConfigDto") -> OutlierModel:
        return OutlierModel.AbsoluteBound
