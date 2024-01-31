from dataclasses import dataclass
from typing import List, Optional
from .MarketDataEntityOutput import MarketDataEntityOutput
from .ArtesianMetadataFacet import ArtesianMetadataFacet


@dataclass
class ArtesianSearchResults:
    """
    Class for the Artesian Search Results.

    Attributes:
        results: list of MarketDataEntityOutput
        facets: list of ArtesianMetadataFacet
        countResults: the count of result
    """

    results: Optional[List[MarketDataEntityOutput]] = None
    facets: Optional[List[ArtesianMetadataFacet]] = None
    countResults: int = 0
