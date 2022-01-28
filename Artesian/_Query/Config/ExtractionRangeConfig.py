from Artesian._GMEPublicOffers import QueryParameters


class ExtractionRangeConfig:
     """ This class sets up the Extraction Range Configuration. 
     
          The DateTime is set in ISO8601 format

           versionFrom:
             the start version timestamp in ISO8601 (ex. "2022-01-01T00:01:02.123456")
          downloadedAt:
             the timestamp of the data in ISO8601 UTC (ex. "2022-01-01T00:01:02.123456Z")
             
          Attributes:
               dateStart: start day for the Date Range extraction.
               dateEnd: end date for the Date Range extraction.
               period: Period range for extraction.
               periodFrom: period start range for extraction.
               periodTo: period end range for extraction.
               relativeInterval: relative interval range for extraction.
               """
     def __init__(self):
        """ Init for the Extraction Range Configuration. 

        """
        self.dateStart = None
        """ Start date for the Date Range for extraction. """
        self.dateEnd = None
        """ End date for Date Renge for extraction. """
        self.period = None
        """ Period range for extraction. """
        self.periodFrom = None
        """ Period start range for extraction. """
        self.periodTo = None
        """ Period end range for extraction. """
        self.relativeInterval = None
        """ Relative Interval range for extraction. """