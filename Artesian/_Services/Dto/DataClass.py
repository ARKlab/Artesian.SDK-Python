from dataclasses import dataclass, field
from ArtesianTags import ArtesianTags
from typing import Optional


@dataclass
class DataClass:
    tags: Optional[ArtesianTags]


@dataclass
class DataClassNone:
    tags: Optional[ArtesianTags] = field(default_factory=lambda: None)


class NoDataClass:
    def __init__(self, tags: Optional[ArtesianTags] = None):
        self.tags = tags