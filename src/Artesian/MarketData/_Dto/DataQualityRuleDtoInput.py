from dataclasses import dataclass
from typing import Optional
from .DataQualityRuleConfigDto import DataQualityRuleConfigDto
from .._Enum.RuleType import RuleType


@dataclass
class DataQualityRuleDtoInput:
    """
    Represents the write model for creating or updating a Data Quality Rule.

    Attributes:
        id: unique identifier of the rule, assigned by the server on creation
        name: human-readable name of the rule
        type: rule type, used to determine expected configuration subtype
        configuration: polymorphic configuration matching the selected type
        version: monotonically increasing version used for optimistic concurrency
        eTag: entity tag used for optimistic concurrency control
    """

    name: str
    type: RuleType
    configuration: DataQualityRuleConfigDto
    version: int
    id: int = 0
    eTag: Optional[str] = None
