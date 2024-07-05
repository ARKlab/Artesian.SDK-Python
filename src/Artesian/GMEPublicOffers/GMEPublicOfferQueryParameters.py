from __future__ import annotations
from typing import List, Optional
from .ExtractionRangeConfig import ExtractionRangeConfig
from ._Enum.BaType import BaType
from ._Enum.GenerationType import GenerationType
from ._Enum.Market import Market
from ._Enum.Purpose import Purpose
from ._Enum.Scope import Scope
from ._Enum.Status import Status
from ._Enum.UnitType import UnitType
from ._Enum.Zone import Zone


class _GMEPublicOfferQueryParameters:
    """Class for the GME Public Offer Query Parameters.

    Attributes:
        scope: sets scope to be queried
        extractionRangeConfig: Sets the Extraction Range Configuration to be queried.
        status: sets the Status to be queried.
        unitType: sets the unit types to be queried.
        generationType: that sets the generation type to be queried.
        operators: sets the operators to be queried.
        unit: sets the units to be queried.
        zone: sets the zones to be queried.
        market: sets the Market to be queried.
        purpose: sets the Purpose to be queried.
        page: sets the Page to be queried.
        pageSize: sets the Page size to be queried.
        baType: sets the BATypes to be queried.
    """

    def __init__(
        self: _GMEPublicOfferQueryParameters,
        page: Optional[int] = None,
        pageSize: Optional[int] = None,
        extractionRangeConfig: Optional[ExtractionRangeConfig] = None,
        scope: Optional[List[Scope]] = None,
        status: Optional[Status] = None,
        unitType: Optional[List[UnitType]] = None,
        generationType: Optional[List[GenerationType]] = None,
        operators: Optional[List[str]] = None,
        unit: Optional[List[str]] = None,
        zone: Optional[List[Zone]] = None,
        market: Optional[List[Market]] = None,
        purpose: Optional[Purpose] = None,
        baType: Optional[List[BaType]] = None,
    ) -> None:
        """
        Inits the GME Public Offer Query Parameters with optional overrides.

        Args:
            page: An int that sets the Page to be queried.
            pageSize: An int that sets the Page size to be queried.
            extractionRangeConfig: Sets the Extraction Range to be queried.
            scope: An enum that sets scope to be queried
            status:An enum that sets the Status to be queried.
            unitType: An enum that sets the unit types to be queried.
            generationType: An enum that sets the generation type to be queried.
            operators: A string that sets the operators to be queried.
            unit: A string that sets the units to be queried.
            zone: An enum that sets the zones to be queried.
            market: An enum that sets the Market to be queried.
            purpose: An enum that sets the Purpose to be queried.
            baType: An enum that sets the BATypes to be queried.
        """

        self.page = page
        self.pageSize = pageSize
        self.scope = scope
        self.extractionRangeConfig = extractionRangeConfig or ExtractionRangeConfig()
        self.status = status
        self.unitType = unitType
        self.generationType = generationType
        self.operators = operators
        self.unit = unit
        self.zone = zone
        self.market = market
        self.purpose = purpose
        self.baType = baType
