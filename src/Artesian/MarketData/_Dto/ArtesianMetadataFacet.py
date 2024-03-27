from dataclasses import dataclass
from typing import List, Optional
from .._Enum import ArtesianMetadataFacetType


@dataclass
class ArtesianMetadataFacetCount:
    """
    Class for the ArtesianMetadataFacetCount Entity.

    Attributes:
        value: the value of the ArtesianMetadataFacet
        count: the count of ArtesianMetadataFacet
    """

    value: Optional[str] = None
    count: int = 0


@dataclass
class ArtesianMetadataFacet:
    """
    Class for the Facet Entity.

    Attributes:
        facetName: the name of the facet
        facetType: the type of the facet
        values: list of ArtesianMetadataFacetCount
    """

    facetName: Optional[str] = None
    facetType: Optional[ArtesianMetadataFacetType] = None
    values: Optional[List[ArtesianMetadataFacetCount]] = None
