from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class AuctionQueryParameters(_QueryParameters): 
    """This class sets up the Auction Query Parameters."""

    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId):
        """ Inits AuctionQueryParameters 
        Args:
            ids: int
            
            extractionRangeSelectionCOnfig
            
            extractionRangeType
            
            timezone: IANA Format
            
            filterId
           """

        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)