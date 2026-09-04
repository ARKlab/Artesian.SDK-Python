from dataclasses import dataclass
from typing import Optional
import datetime


@dataclass
class CheckResultExtractTs:
    """
    Compact extraction result for actual (non-versioned) time series.


    Attributes:
        time: The timestamp.
        issueCount: Number of issues found in the aggregated period.
        competenceStart: Start of first competence.
        competenceEnd: End of last competence.
        providerName: The Provider display name.
        curveName: The Curve display name.
        ruleName: The Rule display name.
        assignmentId: The Assignment ID.
        marketDataId: The Market Data ID.
        ruleId: The Rule ID.
    """
    time: datetime.datetime
    issueCount: int
    competenceStart: datetime.datetime
    competenceEnd: datetime.datetime
    providerName: Optional[str] = None
    curveName: Optional[str] = None
    ruleName: Optional[str] = None
    assignmentId: int = 0
    marketDataId: int = 0
    ruleId: int = 0


@dataclass
class CheckResultExtractVts:
    """
    Compact extraction result for versioned time series (VTS).
    Adds the Version field compared to Ts.


    Attributes:
        time: The timestamp.
        issueCount: Number of issues found in the aggregated period.
        competenceStart: Start of first competence.
        competenceEnd: End of last competence.
        version: The Version timestamp.
        providerName: The Provider display name.
        curveName: The Curve display name.
        ruleName: The Rule display name.
        assignmentId: The Assignment ID.
        marketDataId: The Market Data ID.
        ruleId: The Rule ID.
    """
    time: datetime.datetime
    issueCount: int
    competenceStart: datetime.datetime
    competenceEnd: datetime.datetime
    providerName: Optional[str] = None
    curveName: Optional[str] = None
    ruleName: Optional[str] = None
    assignmentId: int = 0
    marketDataId: int = 0
    ruleId: int = 0
    version: Optional[datetime.datetime] = None
