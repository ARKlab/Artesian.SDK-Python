from dataclasses import dataclass
from typing import List, Optional
from .MarketDataEntityOutputEnriched import MarketDataEntityOutputEnriched
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

    results: Optional[List[MarketDataEntityOutputEnriched]] = None
    facets: Optional[List[ArtesianMetadataFacet]] = None
    countResults: int = 0
