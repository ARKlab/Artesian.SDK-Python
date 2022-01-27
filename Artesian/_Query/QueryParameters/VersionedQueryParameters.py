from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
from Artesian._Query.Config.VersionSelectionConfig import VersionSelectionConfig
class VersionedQueryParameters(_QueryParameters): 
    """This class sets up the Versioned Query Parameters.
    """
    def __init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId, granularity, transformId, versionSelectionConfig, versionSelectionType):
        """ Inits VersionedQueryParameters 
        
        Args:

            ids: int
            
            extractionRangeSelectionConfig 

            configurationRangeType

            timezone: always in a IANA Format

            filterId

            granularity: enum 

            transformId

            versionSelectionConfig

            versionSelectionType. """
       
        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId
        self.fill = None
        if(versionSelectionConfig is None):
            self.versionSelectionConfig = VersionSelectionConfig()
        else:
            self.versionSelectionConfig = versionSelectionConfig
        self.versionSelectionType = versionSelectionType