from dataclasses import dataclass
from typing import Optional

from .ArtesianMetadataFacet import ArtesianMetadataFacet
from .MarketDataEntityOutput import MarketDataEntityOutput


@dataclass
class ArtesianSearchResults:
    """
    Class for the Artesian Search Results.

    Attributes:
        results: list of MarketDataEntityOutput
        facets: list of ArtesianMetadataFacet
        countResults: the count of result
    """

    results: Optional[list[MarketDataEntityOutput]] = None
    facets: Optional[list[ArtesianMetadataFacet]] = None
    countResults: int = 0
