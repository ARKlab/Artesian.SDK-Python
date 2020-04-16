from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class AuctionQueryParameters(_QueryParameters): 
    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId):
        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)