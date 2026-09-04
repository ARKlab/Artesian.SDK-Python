from dataclasses import dataclass

from .._Enum.OutlierModel import OutlierModel
from .OutlierModelConfigDto import OutlierModelConfigDto


@dataclass
class OutlierRefCurveConfigDto(OutlierModelConfigDto):
    """
    Outlier detection model based on a reference Market Data curve.

    A data point is flagged as an outlier if it deviates from the
    reference value by more than tolerancePerc.

    Attributes:
        referenceMarketDataId: id of the reference Market Data entity
        tolerancePerc: maximum allowed percentage deviation from reference
    """

    referenceMarketDataId: int
    tolerancePerc: float

    @property
    def model(self: "OutlierRefCurveConfigDto") -> OutlierModel:
        return OutlierModel.RefCurve
