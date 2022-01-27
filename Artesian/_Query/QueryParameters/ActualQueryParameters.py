import enum

from Artesian import Granularity
from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
class ActualQueryParameters(_QueryParameters): 
    """ This class sets up the Actual Query Parameters.

   //TO CHECK !!!
   """

    def __init__(self, ids: int, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId, granularity: Granularity, transformId):
        """ Inits ActualQueryParameters 
        
        Args:

            ids: int

            extractionRangeSelectionConfig

            extraxtionRangeType

            timezone: IANA Format

            filterId

            granularity: enum
            
            transformId """

        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId
        self.fill = None