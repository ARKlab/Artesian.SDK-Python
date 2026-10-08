from dataclasses import dataclass

from Artesian.MarketData._Dto.CheckResultCheckSummaryDto import CheckResultCheckSummaryDto
from Artesian.MarketData._Dto.CurveRangeEntity import CurveRangeEntity
from Artesian.MarketData._Dto.DataQualityRuleDtoOutput import DataQualityRuleDtoOutput
from Artesian.MarketData._Dto.MarketDataQualityRuleAssignmentDto import (
    MarketDataQualityRuleAssignmentDtoOutput,
)
from Artesian.MarketData._Dto.QualityNotificationAlertAssignmentDto import (
    QualityNotificationAlertAssignmentDtoOutput,
)
from Artesian.MarketData._Dto.QualityNotificationAlertDto import QualityNotificationAlertDtoOutput

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


@dataclass
class PagedResultDataQualityRuleDtoOutput(PagedResult):
    data: list[DataQualityRuleDtoOutput]


@dataclass
class PagedResultMarketDataQualityRuleAssignmentDtoOutput(PagedResult):
    data: list[MarketDataQualityRuleAssignmentDtoOutput]


@dataclass
class PagedResultCheckResultCheckSummaryDto(PagedResult):
    data: list[CheckResultCheckSummaryDto]


@dataclass
class PagedResultQualityNotificationAlertDtoOutput(PagedResult):
    data: list[QualityNotificationAlertDtoOutput]


@dataclass
class PagedResultQualityNotificationAlertAssignmentDtoOutput(PagedResult):
    data: list[QualityNotificationAlertAssignmentDtoOutput]
