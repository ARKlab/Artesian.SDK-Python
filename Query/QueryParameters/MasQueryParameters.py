from Query.QueryParameters.QueryParameters import _QueryParameters
class MasQueryParameters(_QueryParameters): 
    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId, products):
        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.__products=None