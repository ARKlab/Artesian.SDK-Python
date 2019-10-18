from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class ActualQueryParameters(_QueryParameters): 
    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId, granularity, transformId):
        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId