from dataclasses import dataclass
from typing import Optional

from .._Enum.PeriodPrecision import PeriodPrecision
from .CompletenessAndFreshnessConfigDto import CompletenessAndFreshnessConfigDto


@dataclass
class VersionedCompletenessAndFreshnessConfigDto(
    CompletenessAndFreshnessConfigDto
):
    """
    Configuration for Completeness and Freshness rules applied to
    versioned time series.

    Extends the base completeness config with version-specific tolerances
    used to validate version publication windows.

    Attributes:
        versionToleranceFrom: minimum expected version publication offset
            (Period in ISO format)
        versionToleranceTo: maximum expected version publication offset
            (Period in ISO format)
        versionPrecision: optional precision for truncating reference time
            before version tolerance offsets are applied
    """

    versionToleranceFrom: str
    versionToleranceTo: str
    versionPrecision: Optional[PeriodPrecision] = None
