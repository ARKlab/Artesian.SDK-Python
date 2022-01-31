from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.ExtractionRangeType import ExtractionRangeType
from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class AuctionQueryParameters(_QueryParameters): 
    """ 
        Class for the Auction Query Parameters.

        Attributes:
            ids: sets list of marketdata ID's to be queried
            extractionRangeSelectionConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: pecifies the timezone of extracted marketdata.
            filterId: filters marketdata ID to be queries.
            
    """

    def __init__(self, ids: int, 
                       extractionRangeSelectionConfig: ExtractionRangeConfig, 
                       extractionRangeType: ExtractionRangeType, 
                       timezone: str, 
                       filterId: int) -> _QueryParameters:
        """ 
            Inits ActualQueryParameters 
        
            Args:

                ids: An int that sets list of marketdata ID's to be queried
                extractionRangeSelectionConfig: Sets the extraction range configuration.
                extraxtionRangeType: Sets the extraction range type.
                timezone: IANA Format. A string that pecifies the timezone of extracted marketdata.
                filterId: An int that filters marketdata ID to be queries.
        """

        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)