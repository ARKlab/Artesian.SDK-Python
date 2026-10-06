import datetime
from dataclasses import dataclass, field

from Artesian._ClientsExecutor.ArtesianJsonSerializer import WIRE_NAME_KEY


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

    time: datetime.datetime = field(metadata={WIRE_NAME_KEY: "T"})
    issueCount: int = field(metadata={WIRE_NAME_KEY: "D"})
    competenceStart: datetime.datetime = field(metadata={WIRE_NAME_KEY: "S"})
    competenceEnd: datetime.datetime = field(metadata={WIRE_NAME_KEY: "E"})
    providerName: str | None = field(default=None, metadata={WIRE_NAME_KEY: "P"})
    curveName: str | None = field(default=None, metadata={WIRE_NAME_KEY: "C"})
    ruleName: str | None = field(default=None, metadata={WIRE_NAME_KEY: "R"})
    assignmentId: int = field(default=0, metadata={WIRE_NAME_KEY: "AID"})
    marketDataId: int = field(default=0, metadata={WIRE_NAME_KEY: "MKID"})
    ruleId: int = field(default=0, metadata={WIRE_NAME_KEY: "RID"})


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

    time: datetime.datetime = field(metadata={WIRE_NAME_KEY: "T"})
    issueCount: int = field(metadata={WIRE_NAME_KEY: "D"})
    competenceStart: datetime.datetime = field(metadata={WIRE_NAME_KEY: "S"})
    competenceEnd: datetime.datetime = field(metadata={WIRE_NAME_KEY: "E"})
    providerName: str | None = field(default=None, metadata={WIRE_NAME_KEY: "P"})
    curveName: str | None = field(default=None, metadata={WIRE_NAME_KEY: "C"})
    ruleName: str | None = field(default=None, metadata={WIRE_NAME_KEY: "R"})
    assignmentId: int = field(default=0, metadata={WIRE_NAME_KEY: "AID"})
    marketDataId: int = field(default=0, metadata={WIRE_NAME_KEY: "MKID"})
    ruleId: int = field(default=0, metadata={WIRE_NAME_KEY: "RID"})
    version: datetime.datetime | None = field(default=None, metadata={WIRE_NAME_KEY: "V"})
