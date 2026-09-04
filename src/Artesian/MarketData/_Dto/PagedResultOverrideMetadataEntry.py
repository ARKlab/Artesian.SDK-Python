from dataclasses import dataclass
from typing import List

from .OverrideMetadataEntry import OverrideMetadataEntry
from .PagedResult import PagedResult


@dataclass
class PagedResultOverrideMetadataEntry(PagedResult):
    data: List[OverrideMetadataEntry]
