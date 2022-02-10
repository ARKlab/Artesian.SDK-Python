
from .QueryParameters import _QueryParameters
from .ExtractionRangeType import ExtractionRangeType
from .ExtractionRangeConfig import ExtractionRangeConfig
from Artesian.MarketData import Granularity

class ActualQueryParameters(_QueryParameters): 
    """ 
            Class for the Actual Query Parameters.

            Attributes:
                ids: sets list of marketdata ID's to be queried
                extractionRangeSelectionConfig: Sets the extraction range configuration.
                extraxtionRangeType: Sets the extraction range type.
                timezone: specifies the timezone of extracted marketdata.
                filterId: filters marketdata ID to be queries.
                granularity: sets  the granularity to be queried.        
                transformId: sets time range.
    """

    def __init__(self, ids: int, 
                       extractionRangeSelectionConfig: ExtractionRangeConfig, 
                       extractionRangeType: ExtractionRangeType, 
                       timezone: str, 
                       filterId: int, 
                       granularity: Granularity, 
                       transformId: int) -> _QueryParameters: 
        """ 
            Inits ActualQueryParameters 
        
            Args:

                ids: An int that sets list of marketdata ID's to be queried
                extractionRangeSelectionConfig: Sets the extraction range configuration.
                extraxtionRangeType: Sets the extraction range type.
                timezone: IANA Format. A string that specifies the timezone of extracted marketdata.
                filterId: An int that filters marketdata ID to be queries.
                granularity: An enum that sets  the granularity to be queried.        
                transformId: An int that sets time range. 
        """

        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId
        self.fill = None