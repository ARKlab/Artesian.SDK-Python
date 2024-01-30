from dataclasses import dataclass
import datetime
from typing import Optional
from .MarketDataEntityOutput import MarketDataEntityOutput


@dataclass
class ArtesianMetadataFacet:
    """
    Class for the Facet Entity.

    Attributes:
        facetName: the name of the facet
        facetType: the type of the facet
        values: list of ArtesianMetadataFacetCount
    """

    facetName: str = None
    facetType: ArtesianMetadataFacetType = None
    values: Optional[ArtesianMetadataFacetCount] = None


@dataclass
class ArtesianMetadataFacetCount:
    """
    Class for the ArtesianMetadataFacetCount Entity.

    Attributes:
        value: the value of the ArtesianMetadataFacet
        count: the count of ArtesianMetadataFacet
    """
    value: str
    count: int = 0

class ArtesianMetadataFacetType(Enum):
    Property = 0
    Tag = 1
