from dataclasses import dataclass
from datetime import datetime

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
    rows: dict[datetime, float | None] | None = keyValueArrayField()
    version: datetime | None = None
    timezone: str | None = None
