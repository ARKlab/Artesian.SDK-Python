from dataclasses import dataclass, field
from datetime import date, datetime

from Artesian._ClientsExecutor.ArtesianJsonSerializer import WIRE_NAME_KEY

from .._Enum.CheckAggregatedStatus import CheckAggregatedStatus


@dataclass
class DataQualityStatusSummaryDto:
    """
    Provides an at-a-glance quality status summary for a specific Market Data
    entity.

    Attributes:
        lastCheckTime: timestamp of the most recent quality check execution for
            this Market Data
        overallStatus: overall aggregated quality status across all active rule
            assignments (OK if all pass, KO if any fail)
        activeRulesCount: number of currently active quality rule assignments
            bound to this Market Data
        failedRulesCount: number of active rule assignments whose last check
            resulted in a failure (KO)
        from_: start of the validated data range for this Market Data; None if
            no check results are available yet. Serialized from/to API field
            named "From".
        to: end of the validated data range for this Market Data; None if no
            check results are available yet
    """

    lastCheckTime: datetime | None = None
    overallStatus: CheckAggregatedStatus | None = None
    activeRulesCount: int = 0
    failedRulesCount: int = 0
    from_: date | None = field(default=None, metadata={WIRE_NAME_KEY: "From"})
    to: date | None = None
