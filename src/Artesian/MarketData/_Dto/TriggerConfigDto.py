from abc import ABC, abstractmethod
from dataclasses import dataclass

from .._Enum.AlertType import AlertType
from .ScheduleDefinitionDto import ScheduleDefinitionDto


class TriggerConfigDto(ABC):
    """Base class for quality notification alert trigger configurations."""

    @property
    @abstractmethod
    def type(self: "TriggerConfigDto") -> AlertType:
        """Discriminator indicating the alert trigger type."""
        raise NotImplementedError


@dataclass
class OnEventTriggerConfigDto(TriggerConfigDto):
    """Trigger configuration for event-driven alerts."""

    @property
    def type(self: "OnEventTriggerConfigDto") -> AlertType:
        return AlertType.OnEvent


@dataclass
class ScheduleTriggerConfigDto(TriggerConfigDto):
    """Trigger configuration for scheduled alert digests."""

    scheduleDefinition: ScheduleDefinitionDto

    @property
    def type(self: "ScheduleTriggerConfigDto") -> AlertType:
        return AlertType.Scheduled
