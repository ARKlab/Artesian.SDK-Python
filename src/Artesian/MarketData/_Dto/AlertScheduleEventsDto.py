from dataclasses import dataclass, field
from datetime import datetime

from .PagedResult import PagedResultDqCheckChangeEventDtoOutput


@dataclass
class AlertScheduleEventsDtoOutput:
    """Read model containing materialized DQ events for one schedule
    occurrence.

    Attributes:
        scheduleTime: The schedule occurrence timestamp this event set was
                      materialized for
        events: The DQ check change events for this schedule occurrence
    """

    scheduleTime: datetime | None = None
    events: PagedResultDqCheckChangeEventDtoOutput = field(default_factory=PagedResultDqCheckChangeEventDtoOutput)


AlertScheduleEventsOutput = AlertScheduleEventsDtoOutput
