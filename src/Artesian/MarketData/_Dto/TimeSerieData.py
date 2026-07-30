from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
from Artesian.MarketData._Enum.MarketDataTypeV2 import MarketDataTypeV2


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

    type: MarketDataTypeV2
    rows: Optional[Dict[datetime, Optional[float]]] = None
    version: Optional[datetime] = None
    timezone: Optional[str] = None
