from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from .._Enum.OverrideKind import OverrideKind
from .UpsertData import UpsertData


@dataclass
class UpsertCurveDataOverride(UpsertData):
    """
    Payload for upserting an override or fallback correction.

    Inherits all curve data fields from UpsertData and adds the
    override-specific metadata required to describe the correction.

    Attributes:
        kind: whether the write is an override or a fallback.
        overrideId: identifier of an existing override or fallback to update,
            merge, or replace. When None, a new entry is created.
        replaceExisting: when True, an overlapping correction of the same kind is
            trimmed or replaced to remain consistent with this write.
        comment: optional free-text comment describing the reason for the
            override or fallback.
    """

    kind: OverrideKind = OverrideKind.Override
    overrideId: UUID | None = None
    replaceExisting: bool = False
    comment: str | None = None

    def validate(self: UpsertCurveDataOverride) -> None:
        if self.overrideId is not None and self.overrideId.int == 0:
            raise ValueError("Override metadata id must be valorized")
