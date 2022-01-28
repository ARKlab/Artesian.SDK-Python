import enum

from Artesian import Granularity
from Artesian._GMEPublicOffers import QueryParameters
from Artesian._GMEPublicOffers.Config.ExtractionRangeConfig import ExtractionRangeConfig
from Artesian._Query.Config.ExtractionRangeType import ExtractionRangeType

from Artesian._Query.QueryParameters.QueryParameters import _QueryParameters

class ActualQueryParameters(_QueryParameters): 
    """ Class for the Actual Query Parameters.

            Attributes:
                ids: sets list of marketdata ID's to be queried
                extractionRangeSelectionConfig: Sets the extraction range configuration.
                extraxtionRangeType: Sets the extraction range type.
                timezone: specifies the timezone of extracted marketdata.
                filterId: filters marketdata ID to be queries.
                granularity: sets  the granularity to be queried.        
                transformId: sets time range.

                Returns:
                    Query Type """

    def __init__(self, ids: int, extractionRangeSelectionConfig: ExtractionRangeConfig, extractionRangeType: ExtractionRangeType, timezone: str, filterId: int, granularity: Granularity, transformId: int) -> _QueryParameters: 
        """ Inits ActualQueryParameters 
        
        Args:

            ids: An int that sets list of marketdata ID's to be queried
            extractionRangeSelectionConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: IANA Format. A string that specifies the timezone of extracted marketdata.
            filterId: An int that filters marketdata ID to be queries.
            granularity: An enum that sets  the granularity to be queried.        
            transformId: An int that sets time range. """

        _QueryParameters.__init__(self, ids, extractionRangeSelectionConfig, extractionRangeType, timezone, filterId)
        self.granularity = granularity
        self.transformId = transformId
        self.fill = None