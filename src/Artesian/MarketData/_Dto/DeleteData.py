from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from Artesian.MarketData._Dto import MarketDataIdentifier


@dataclass
class DeleteData:
    """
    Class for the Delete Data.

    Attributes:
        ID: the MarketDataIdentifier
        timezone: the Timezone of the rows. Must be the OriginalTimezone
                  when writing Dates or must be ""UTC"" when writing Times
        rangeStart: LocalDateTime start of the range to be deleted
        rangeEnd: LocalDateTime end of the range to be deleted
        product: The list of Product. Only *,
                 is special character for 'delete all products in the range'
        version: the Version to operate on
        deferCommandExecution: flag to choose between synchronous
                               and asynchronous command execution
        deferDataGeneration: flag to choose between synchronous
                             and asynchronous data generation (MUV)
    """

    ID: MarketDataIdentifier
    timezone: str
    rangeStart: datetime
    rangeEnd: datetime
    product: Optional[List[str]] = None
    version: Optional[datetime] = None
    deferCommandExecution: bool = False
    deferDataGeneration: bool = True
