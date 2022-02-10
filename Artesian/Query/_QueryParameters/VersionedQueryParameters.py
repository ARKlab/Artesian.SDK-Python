from .ExtractionRangeConfig import ExtractionRangeConfig
from .QueryParameters import _QueryParameters
from .VersionSelectionConfig import VersionSelectionConfig
from .ExtractionRangeType import ExtractionRangeType
from .VersionSelectionType import VersionSelectionType
from Artesian.MarketData import Granularity

class VersionedQueryParameters(_QueryParameters): 
    """
        Class for the Versioned Query Parameters.

        Attributes:
            ids: sets list of marketdata ID's to be queried
            extractionRangeSelectionConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: specifies the timezone of extracted marketdata.
            filterId: filters marketdata ID to be queries.
            granularity: sets  the granularity to be queried.        
            transformId: sets time range.
            versionSelectionConfig: Sets the version selectuon configuration.
            versionSelectionType: Sets the version selection time.

    """

    def __init__(self, ids: int, 
                       extractionRangeSelectionConfig : ExtractionRangeConfig, 
                       extractionRangeType: ExtractionRangeType, 
                       timezone: str, 
                       filterId: int, 
                       granularity: Granularity, 
                       transformId: int, 
                       versionSelectionConfig: VersionSelectionConfig, 
                       versionSelectionType: VersionSelectionType) -> _QueryParameters:
        """ 
            Inits ActualQueryParameters 
        
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