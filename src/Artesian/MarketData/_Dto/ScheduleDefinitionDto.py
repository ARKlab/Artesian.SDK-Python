from dataclasses import dataclass

from .._Enum.ScheduleDefinitionType import ScheduleDefinitionType


@dataclass
class ScheduleDefinitionDto:
    """
    Base class for schedule definition DTOs.
    """

    @property
    def type(self: "ScheduleDefinitionDto") -> ScheduleDefinitionType:
        raise NotImplementedError(
            "ScheduleDefinitionDto.type must be implemented by subclasses"
        )
