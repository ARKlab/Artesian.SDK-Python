from .ExtractionRangeConfig import ExtractionRangeConfig
from .ExtractionRangeType import ExtractionRangeType


class _QueryParameters: 
    def __init__(self, ids: int, 
                       extractionRangeSelectionConfig: ExtractionRangeConfig, 
                       extractionRangeType: ExtractionRangeType, 
                       timezone: str, 
                       filterId: int):
                       
        self.ids = ids
        self.extractionRangeSelectionConfig = extractionRangeSelectionConfig
        self.extractionRangeType = extractionRangeType
        self.timezone = timezone
        self.filterId = filterId
