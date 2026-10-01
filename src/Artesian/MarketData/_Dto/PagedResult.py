from dataclasses import dataclass

from Artesian.MarketData._Dto.CurveRangeEntity import CurveRangeEntity

# Concrete subclasses per payload (the former jsons serializer failed with Generics);
# kept to preserve the public types.


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
    data: list[CurveRangeEntity]
