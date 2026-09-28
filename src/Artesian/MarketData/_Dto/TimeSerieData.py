from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from Artesian._ClientsExecutor.ArtesianJsonSerializer import keyValueArrayField
from Artesian.MarketData._Enum.MarketDataType import MarketDataType


@dataclass
class TimeSerieData:
    """
    Class Timeserie data.

    Attributes:
        rows: The timeserie data in OriginalTimezone or, when Hourly, UTC.
        type: MarketDataEntity Type
        version: The Version to operate on
        timezone: The timezone of the Rows. Must be the OriginalTimezone or, when Hourly, must be "UTC".
    """

    type: MarketDataType
    rows: Optional[dict[datetime, Optional[float]]] = keyValueArrayField()
    version: Optional[datetime] = None
    timezone: Optional[str] = None
