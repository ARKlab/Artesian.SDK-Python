from dataclasses import dataclass

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

    results: list[MarketDataEntityOutput] | None = None
    facets: list[ArtesianMetadataFacet] | None = None
    countResults: int = 0
