from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class MasQueryParameters(_QueryParameters): 
    """This class sets up the Mas Query Parameters."""

    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId, products):
        """ Inits MasQueryParameters.
        
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
