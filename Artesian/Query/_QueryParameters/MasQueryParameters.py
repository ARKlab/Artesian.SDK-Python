from typing import List
from .ExtractionRangeConfig import ExtractionRangeConfig
from .QueryParameters import _QueryParameters
from .ExtractionRangeType import ExtractionRangeType

class MasQueryParameters(_QueryParameters): 
    """ 
        Class for the Mas Query Parameters.

        Attributes:
            ids: sets list of marketdata ID's to be queried
            extractionRangeConfig: Sets the extraction range configuration.
            extraxtionRangeType: Sets the extraction range type.
            timezone: specifies the timezone of extracted marketdata.
            filterId: filters marketdata ID to be queries.
            products: sets products to be queried.
    """
    def __init__(self, ids: List[int] = None, 
                       extractionRangeConfig: ExtractionRangeConfig = ExtractionRangeConfig(), 
                       extractionRangeType: ExtractionRangeType = None, 
                       timezone: str = None, 
                       filterId: int = None, 
                       products: List[str] = None) -> None:
        """ 
            Inits ActualQueryParameters 
        
            Args:

                ids: An int that sets list of marketdata ID's to be queried
                extractionRangeConfig: Sets the extraction range configuration.
                extraxtionRangeType: Sets the extraction range type.
                timezone: IANA Format. A string specifies the timezone of extracted marketdata.
                filterId: An int that filters marketdata ID to be queries.
                products: A string that sets products to be queried.
        """
        _QueryParameters.__init__(self, ids, extractionRangeConfig, extractionRangeType, timezone, filterId)
        self.products = products
