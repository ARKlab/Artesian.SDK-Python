from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Services.Enum.BaType import BaType
from Artesian._Services.Enum.GenerationType import GenerationType
from Artesian._Services.Enum.Market import Market
from Artesian._Services.Enum.Purpose import Purpose
from Artesian._Services.Enum.Scope import Scope
from Artesian._Services.Enum.Status import Status
from Artesian._Services.Enum.UnitType import UnitType
from Artesian._Services.Enum.Zone import Zone


class GMEPOfferQueryParameters: 
    """ Class for the GME Public Offer Query Parameters.
    
        Attributes:
            scope: sets scope to be queried
            extractionRangeSelectionConfig: Sets the Extraction Range Selection Configuration to be queried.
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


    def __init__(self, page: int, 
                       pageSize: int,
                       scope: Scope, 
                       extractionRangeSelectionConfig: ExtractionRangeConfig, 
                       status: Status, 
                       unitType: UnitType, 
                       generationType: GenerationType, 
                       operator: str, 
                       unit: str, 
                       zone: Zone , 
                       market: Market, 
                       purpose: Purpose, 
                       baType: BaType)  -> None : 
        """ 
            Inits the GME Public Offer Query Parameters with optional overrides.
       
            Args:
                scope: An enum that sets scope to be queried
                extractionRangeSelectionConfig: Sets the Extraction Range Selection Configuration to be queried.
                status:An enum that sets the Status to be queried.
                unitType: An enum that sets the unit types to be queried.
                generationType: An enum that sets the generation type to be queried.
                operator: A string that sets the operators to be queried.
                unit: A string that sets the units to be queried.
                zone: An enum that sets the zones to be queried.
                market: An enum that sets the Market to be queried.
                purpose: An enum that sets the Purpose to be queried.
                page: An int that sets the Page to be queried.
                pageSize: An int that sets the Page size to be queried.
                baType: An enum that sets the BATypes to be queried.
        """

        self.page = page
        self.pageSize = pageSize
        self.scope = scope
        self.extractionRangeSelectionConfig = extractionRangeSelectionConfig
        self.status = status
        self.unitType = unitType
        self.generationType = generationType
        self.operator = operator
        self.unit = unit
        self.zone = zone
        self.market = market
        self.purpose = purpose
        self.baType = baType
         