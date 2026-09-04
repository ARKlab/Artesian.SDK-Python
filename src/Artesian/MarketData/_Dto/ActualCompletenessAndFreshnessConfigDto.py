from dataclasses import dataclass

from .CompletenessAndFreshnessConfigDto import CompletenessAndFreshnessConfigDto


@dataclass
class ActualCompletenessAndFreshnessConfigDto(CompletenessAndFreshnessConfigDto):
    """
    Configuration for Completeness and Freshness rules applied to
    actual (non-versioned) time series.

    Inherits schedule and record validation settings from
    CompletenessAndFreshnessConfigDto.
    """

    pass
