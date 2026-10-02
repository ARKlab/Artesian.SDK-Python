from dataclasses import dataclass

from .OverrideMetadataEntry import OverrideMetadataEntry
from .PagedResult import PagedResult


@dataclass
class PagedResultOverrideMetadataEntry(PagedResult):
    data: list[OverrideMetadataEntry]
