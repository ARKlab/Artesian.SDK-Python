
class ExtractionRangeConfig:
     """ This class sets up the Extraction Range Configuration. 
            
          Attributes:
               dateStart: start day for the Date Range extraction.
               dateEnd: end date for the Date Range extraction.
               period: Period range for extraction.
               periodFrom: period start range for extraction.
               periodTo: period end range for extraction.
               relativeInterval: relative interval range for extraction.
     """
     def __init__(self):
        """ Init for the Extraction Range Configuration. """
        self.dateStart:str = None
        """ Start date for the Date Range for extraction. (ISO format) """
        self.dateEnd:str = None
        """ End date for Date Renge for extraction. (ISO format)"""
        self.period:str = None
        """ Period range for extraction. (ISO format)"""
        self.periodFrom:str = None
        """ Period start range for extraction. (ISO format)"""
        self.periodTo:str = None
        """ Period end range for extraction. (ISO format)"""
        self.relativeInterval:str = None
        """ Relative Interval range for extraction."""