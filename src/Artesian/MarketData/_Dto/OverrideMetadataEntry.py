from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from .._Enum.OverrideKind import OverrideKind


@dataclass
class OverrideMetadataEntry:
    """
    Metadata record identifying an override or fallback applied to Market Data.

    This is the current-state descriptor of a correction, not a full audit
    trail. Records can be replaced, and deleting a record does not reinstate
    prior overrides.

    Attributes:
        id: unique identifier assigned by the server on write.
        marketDataId: identifier of the Market Data referenced by this entry.
        kind: whether this entry is an override or a fallback.
        version: version for versioned data; null for Actual and MAS data.
        product: product for MAS and BidAsk data; empty for Actual and Versioned data.
        referencedMarketDataId: referenced Market Data identifier in the curve-range link.
        rangeExactStart: effective range start.
        rangeExactEnd: effective range end.
        createdBy: principal that created the override or fallback.
        createdAt: UTC timestamp when the entry was created.
        comment: optional free-text comment describing the correction.
    """

    id: Optional[UUID]
    marketDataId: int
    kind: OverrideKind
    version: Optional[datetime]
    product: Optional[str]
    referencedMarketDataId: int
    rangeExactStart: datetime
    rangeExactEnd: datetime
    createdBy: Optional[str]
    createdAt: datetime
    comment: Optional[str] = None
