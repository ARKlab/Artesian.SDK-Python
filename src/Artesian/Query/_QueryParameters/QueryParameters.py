from __future__ import annotations
from typing import List, Optional

from .ExtractionRangeConfig import ExtractionRangeConfig
from .ExtractionRangeType import ExtractionRangeType


class _FillStrategy:
    def getUrlParams(self: _FillStrategy) -> str:
        raise NotImplementedError("Please Implement this method")


class _NullFillStrategy(_FillStrategy):
    def getUrlParams(self: _NullFillStrategy) -> str:
        return "fillerK=Null"


class _NoFillStrategy(_FillStrategy):
    def getUrlParams(self: _NoFillStrategy) -> str:
        return "fillerK=NoFill"


class _FillLatestStrategy(_FillStrategy):
    def __init__(self: _FillLatestStrategy, period: str, continueToEnd: bool) -> None:
        self.period = period
        self.continueToEnd = continueToEnd

    def getUrlParams(self: _FillLatestStrategy) -> str:
        return (
            f"fillerK=LatestValidValue&fillerP={self.period}"
            + f"&fillerC={self.continueToEnd}"
        )


class _FillCustomTimeserieStrategy(_FillStrategy):
    def __init__(self: _FillCustomTimeserieStrategy, val: float) -> None:
        self.val = val

    def getUrlParams(self: _FillCustomTimeserieStrategy) -> str:
        return f"fillerK=CustomValue&fillerDV={self.val}"


def toQueryParams(vals: List[List[str | float | int | None]]) -> str:
    filtered = filter(lambda x: x[1], vals)
    stringVals = map(lambda x: [x[0], str(x[1])], filtered)
    joinedEqual = map(lambda x: "=".join(x), stringVals)
    return "&".join(joinedEqual)


class _FillCustomBidAskStrategy(_FillStrategy):
    def __init__(self: _FillCustomBidAskStrategy, **val: float) -> None:
        self.val = val

    def getUrlParams(self: _FillCustomBidAskStrategy) -> str:
        return toQueryParams(
            [
                ["fillerK", "CustomValue"],
                ["fillerDVbbp", self.val.get("bestBidPrice")],
                ["fillerDVbap", self.val.get("bestAskPrice")],
                ["fillerDVbbq", self.val.get("bestBidQuantity")],
                ["fillerDVbaq", self.val.get("bestAskQuantity")],
                ["fillerDVlp", self.val.get("lastPrice")],
                ["fillerDVlq", self.val.get("lastQuantity")],
            ]
        )


class _FillCustomMasStrategy(_FillStrategy):
    def __init__(self: _FillCustomMasStrategy, **val: float) -> None:
        self.val = val

    def getUrlParams(self: _FillCustomMasStrategy) -> str:
        return toQueryParams(
            [
                ["fillerK", "CustomValue"],
                ["fillerDVs", self.val.get("settlement")],
                ["fillerDVo", self.val.get("open")],
                ["fillerDVc", self.val.get("close")],
                ["fillerDVh", self.val.get("high")],
                ["fillerDVl", self.val.get("low")],
                ["fillerDVvp", self.val.get("volumePaid")],
                ["fillerDVvg", self.val.get("volumeGiven")],
                ["fillerDVvt", self.val.get("volume")],
            ]
        )


class _QueryParameters:
    def __init__(
        self: _QueryParameters,
        ids: Optional[List[int]],
        extractionRangeConfig: ExtractionRangeConfig = ExtractionRangeConfig(),
        extractionRangeType: Optional[ExtractionRangeType] = None,
        timezone: Optional[str] = None,
        filterId: Optional[int] = None,
        fill: Optional[_FillStrategy] = None,
    ) -> None:
        self.ids = ids
        self.extractionRangeConfig = extractionRangeConfig
        self.extractionRangeType = extractionRangeType
        self.timezone = timezone
        self.filterId = filterId
        self.fill = fill
