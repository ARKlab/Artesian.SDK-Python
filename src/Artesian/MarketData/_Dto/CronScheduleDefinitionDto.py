from __future__ import annotations

from dataclasses import dataclass

from .._Enum.ScheduleDefinitionType import ScheduleDefinitionType
from .ScheduleDefinitionDto import ScheduleDefinitionDto


@dataclass
class CronScheduleDefinitionDto(ScheduleDefinitionDto):
    """
    A schedule definition based on a cron expression, specifying recurring
    check times in a given time zone.

    Attributes:
        cronExpression: cron expression defining the schedule pattern
        timeZone: IANA time zone identifier used to evaluate cronExpression
    """

    cronExpression: str | None = None
    timeZone: str | None = None

    @property
    def type(self: CronScheduleDefinitionDto) -> ScheduleDefinitionType:
        return ScheduleDefinitionType.Cron
