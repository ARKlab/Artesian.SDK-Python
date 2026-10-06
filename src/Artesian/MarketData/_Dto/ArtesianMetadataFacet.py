from dataclasses import dataclass

from .._Enum import ArtesianMetadataFacetType


@dataclass
class ArtesianMetadataFacetCount:
    """
    Class for the ArtesianMetadataFacetCount Entity.

    Attributes:
        value: the value of the ArtesianMetadataFacet
        count: the count of ArtesianMetadataFacet
    """

    value: str | None = None
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

    facetName: str | None = None
    facetType: ArtesianMetadataFacetType | None = None
    values: list[ArtesianMetadataFacetCount] | None = None
