from Artesian._GMEPublicOffers import QueryParameters


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
        self.dateStart = None
        """ Start date for the Date Range for extraction. (ISO format) """
        self.dateEnd = None
        """ End date for Date Renge for extraction. (ISO format)"""
        self.period = None
        """ Period range for extraction. (ISO format)"""
        self.periodFrom = None
        """ Period start range for extraction. (ISO format)"""
        self.periodTo = None
        """ Period end range for extraction. (ISO format)"""
        self.relativeInterval = None
        """ Relative Interval range for extraction."""