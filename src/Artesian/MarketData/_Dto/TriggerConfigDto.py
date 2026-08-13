from abc import ABC, abstractmethod

from .._Enum.AlertType import AlertType


class TriggerConfigDto(ABC):
    """Base class for quality notification alert trigger configurations."""

    @property
    @abstractmethod
    def type(self: "TriggerConfigDto") -> AlertType:
        """Discriminator indicating the alert trigger type."""
        raise NotImplementedError
