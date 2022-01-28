from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.ExtractionRangeType import ExtractionRangeType
from Artesian._Query.Config.Granularity import Granularity
from Artesian._Query.Config.VersionSelectionType import VersionSelectionType
from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters
from Artesian._Query.Config.VersionSelectionConfig import VersionSelectionConfig
class VersionedQueryParameters(_QueryParameters): 
    """This class sets up the Versioned Query Parameters.
    
        Returns:
            Query Type."""
    def __init__(self, ids: int, extractionRangeSelectionConfig : ExtractionRangeConfig, extractionRangeType: ExtractionRangeType, timezone: str, filterId: int, granularity: Granularity, transformId: int, versionSelectionConfig: VersionSelectionConfig, versionSelectionType: VersionSelectionType) -> _QueryParameters:
        """ Inits ActualQueryParameters 
        
        Args:

            ids: An int that ets list of marketdata ID's to be queried
            extractionRangeSelectionConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA Format. A string pecifies the timezone of extracted marketdata.
            filterId: An int that filters marketdata ID to be queries.
            granularity: An enum that sets  the granularity to be queried.        
            transformId: An int that sets time range.
            versionSelectionConfig: Sets the version selectuon configuration.
            versionSelectionType: Sets the version selection time.
        """
       
        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId
        self.fill = None
        if(versionSelectionConfig is None):
            self.versionSelectionConfig = VersionSelectionConfig()
        else:
            self.versionSelectionConfig = versionSelectionConfig
        self.versionSelectionType = versionSelectionType