from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class BidAskQueryParameters(_QueryParameters): 
    """This class sets up the Bid Ask Query Parameters."""

    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId, products):
        """ Inits BidAskQueryParameters
        
        Args:
            ids: int
            
            extractionRangeSelectionCOnfig
            
            extractionRangeType
            
            timezone: IANA Format
            
            filterId
            
            products """

        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.__products=None
        self.fill = None
