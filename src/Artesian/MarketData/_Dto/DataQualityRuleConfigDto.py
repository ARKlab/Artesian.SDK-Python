from dataclasses import dataclass

from .._Enum.RuleType import RuleType


@dataclass
class DataQualityRuleConfigDto:
    """
    Class for the Data Quality Rule Configuration.

    Attributes:
        type: Discriminator indicating the rule type. Determines which configuration properties are relevant.

    """

    type: RuleType
