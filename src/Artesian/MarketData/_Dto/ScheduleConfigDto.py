from dataclasses import dataclass

from .ScheduleDefinitionDto import ScheduleDefinitionDto


@dataclass
class ScheduleConfigDto:
    """
    Defines when and how often a quality check should be executed.

    Combines a schedule definition with a maximum allowed delay.

    Attributes:
        scheduleDefinition: schedule pattern (cron or custom definition)
        maxDelay: maximum acceptable delay (Period in ISO format)
    """

    scheduleDefinition: ScheduleDefinitionDto
    maxDelay: str
