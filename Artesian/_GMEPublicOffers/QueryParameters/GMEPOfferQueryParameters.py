from numpy import int0
from Artesian._GMEPublicOffers.Config.BaType import BaType
from Artesian._GMEPublicOffers.Config.GenerationType import GenerationType
from Artesian._GMEPublicOffers.Config.Market import Market
from Artesian._GMEPublicOffers.Config.Purpose import Purpose
from Artesian._GMEPublicOffers.Config.Scope import Scope
from Artesian._GMEPublicOffers.Config.Status import Status
from Artesian._GMEPublicOffers.Config.UnitType import UnitType
from Artesian._GMEPublicOffers.Config.Zone import Zone


class GMEPOfferQueryParameters: 
    def __init__(self, scope: Scope, extractionRangeSelectionConfig, status: Status, unitType: UnitType, generationType: GenerationType, operator: str, unit, zone: Zone , market: Market, purpose: Purpose, page: int, pageSize: int, baType: BaType):
        """ 
       Inits the GME Public Offer Query Parameters with optional overrides.
       

       // RITOCCARE CON ENUM! TO CHECK !!
       Args:
            scope: An enum that sets scope to be queried "(from 1 to 9)".
            extractionRangeSelectionConfig: A (?) that sets the Extraction Range Selection Configuration to be queried.
            status:An enum that sets the Status to be queried "(from 1 to 6)".
            unitType: An enum that sets the unit types to be queried "(from 1 to 4)".
            generationType: An enum that sets the generation type to be queried "(from 1 to 13)".
            operator: A string that sets the operators to be queried.
            unit: A (?) that sets the units to be queried.
            zone: An enum that sets the zones to be queried "(from 1 to 19)".
            market: An enum that sets the Market to be queried "(from 1 to 16)".
            purpose: An enum that sets the Purpose to be queried "(1 or 2)".
            page: An int that sets the Page to be queried.
            pageSize: An int that sets the Page size to be queried.
            baType: An enum that sets the BATypes to be queried "(from 1 to 4)"."""

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
        self.page = page
        self.pageSize = pageSize
        self.baType = baType
         