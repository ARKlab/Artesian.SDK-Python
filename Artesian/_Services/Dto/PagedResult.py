from dataclasses import dataclass
from typing import List

from Artesian._Services.Dto.CurveRangeEntity import CurveRangeEntity

# Has been tried extensively to use TypeVar and Generic for this purpose
# jsons library fails with Generics thus we opted for the following

@dataclass
class PagedResult:
    page:int
    pageSize:int
    count:int
    isCountPartial:bool
      
@dataclass
class PagedResultCurveRangeEntity(PagedResult):
    data:List[CurveRangeEntity]