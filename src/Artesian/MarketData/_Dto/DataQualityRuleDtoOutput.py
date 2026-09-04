from dataclasses import dataclass
from typing import Optional

from .._Enum.CheckAggregatedStatus import CheckAggregatedStatus
from .DataQualityRuleDtoInput import DataQualityRuleDtoInput


@dataclass
class DataQualityRuleDtoOutput(DataQualityRuleDtoInput):
    """
    Read model returned by GET operations.

    Extends DataQualityRuleDtoInput with the latest aggregated status
    computed across all assignments of the rule.

    Attributes:
        aggregatedStatus: latest aggregated check status, None if no check
            has been executed yet
    """

    aggregatedStatus: Optional[CheckAggregatedStatus] = None
