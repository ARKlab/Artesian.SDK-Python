from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .DqCheckChangeEventDto import DqCheckChangeEventDtoOutput


@dataclass
class AlertScheduleEventsDtoOutput:
    """
    Read model containing materialized DQ events for one schedule occurrence.

    Attributes:
        scheduleTime: The schedule occurrence timestamp this event set was materialized for
        events: The DQ check change events for this schedule occurrence
    """

    scheduleTime: Optional[datetime] = None
    events: List[DqCheckChangeEventDtoOutput] = field(default_factory=list)


AlertScheduleEventsOutput = AlertScheduleEventsDtoOutput
