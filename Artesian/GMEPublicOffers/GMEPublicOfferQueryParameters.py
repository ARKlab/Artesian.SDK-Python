from typing import List
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
    """ Class for the GME Public Offer Query Parameters.
    
        Attributes:
            scope: sets scope to be queried
            extractionRangeConfig: Sets the Extraction Range Selection Configuration to be queried.
            status: sets the Status to be queried.
            unitType: sets the unit types to be queried.
            generationType: that sets the generation type to be queried.
            operator: sets the operators to be queried.
            unit: sets the units to be queried.
            zone: sets the zones to be queried.
            market: sets the Market to be queried.
            purpose: sets the Purpose to be queried.
            page: sets the Page to be queried.
            pageSize: sets the Page size to be queried.
            baType: sets the BATypes to be queried.
    """

    def __init__(self, page: int = None, 
                       pageSize: int = None,
                       extractionRangeConfig: ExtractionRangeConfig = None, 
                       scope: List[Scope] = None, 
                       status: Status = None, 
                       unitType: List[UnitType] = None, 
                       generationType: List[GenerationType] = None, 
                       operator: List[str] = None, 
                       unit: List[str] = None, 
                       zone: List[Zone] = None, 
                       market: List[Market] = None, 
                       purpose: Purpose = None, 
                       baType: List[BaType] = None)  -> None: 
        """ 
            Inits the GME Public Offer Query Parameters with optional overrides.
       
            Args:
                page: An int that sets the Page to be queried.
                pageSize: An int that sets the Page size to be queried.
                extractionRangeConfig: Sets the Extraction Range Selection Configuration to be queried.
                scope: An enum that sets scope to be queried
                status:An enum that sets the Status to be queried.
                unitType: An enum that sets the unit types to be queried.
                generationType: An enum that sets the generation type to be queried.
                operator: A string that sets the operators to be queried.
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
        self.operator = operator
        self.unit = unit
        self.zone = zone
        self.market = market
        self.purpose = purpose
        self.baType = baType
         