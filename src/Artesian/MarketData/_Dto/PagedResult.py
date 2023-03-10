from dataclasses import dataclass
from typing import List

from Artesian.MarketData._Dto.CurveRangeEntity import CurveRangeEntity

# Has been tried extensively to use TypeVar and Generic for this purpose
# jsons library fails with Generics thus we opted for the following


@dataclass
class PagedResult:
    """
    Class for the paged result.

    Attributes:
        page: page number (1-based)
        pageSize: page size (nu,ber of elements by page)
        count: number of pages
        isCountPartial: indicates if the count is partia
        data: data
    """

    page: int
    pageSize: int
    count: int
    isCountPartial: bool


@dataclass
class PagedResultCurveRangeEntity(PagedResult):
    data: List[CurveRangeEntity]
