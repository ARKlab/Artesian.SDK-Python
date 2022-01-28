from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.ExtractionRangeType import ExtractionRangeType
from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class BidAskQueryParameters(_QueryParameters): 
    """This class sets up the Bid Ask Query Parameters.
        
        Returns:
            Query Type."""

    def __init__(self, ids: int, extractionRangeSelectionConfig: ExtractionRangeConfig, extractionRangeType: ExtractionRangeType, timezone: str, filterId: int, products: str) -> _QueryParameters:
        """ Inits ActualQueryParameters 
        
        Args:

            ids: An int that ets list of marketdata ID's to be queried
            extractionRangeSelectionConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA Format. A string pecifies the timezone of extracted marketdata.
            filterId: An int that filters marketdata ID to be queries.
            products: A string that sets products to be queried.
        """


        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.__products=None
        self.fill = None
