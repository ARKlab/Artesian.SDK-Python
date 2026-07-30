from dataclasses import dataclass
from typing import Optional

from Artesian.MarketData._Dto.DataQualityStatusSummaryDto import DataQualityStatusSummaryDto


@dataclass
class DqRuleDqStatusSummaryDto:
    """
    Lightweight DTO pairing a Data Quality Rule with its aggregated DQ status summary.
    Used by the DqRule DQ Status Summary endpoint.


    Attributes:
        ruleId: The Data Quality Rule identifier.
        statusSummary: The aggregated DQ status summary for this rule
                       (across all assigned Market Data, or filtered by a specific Market Data).
    """
    ruleId: int
    statusSummary: Optional[DataQualityStatusSummaryDto] = None
