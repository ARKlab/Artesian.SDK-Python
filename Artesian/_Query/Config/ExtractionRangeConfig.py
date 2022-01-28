from Artesian._GMEPublicOffers import QueryParameters


class ExtractionRangeConfig:
     """ This class sets up the Extraction Range Configuration. """
     def __init__(self):
        """ Init for the Extraction Range Configuration. 

        The DateTime is set in ISO8601 format

        versionFrom:
             the start version timestamp in ISO8601 (ex. "2022-01-01T00:01:02.123456")
        downloadedAt:
             the timestamp of the data in ISO8601 UTC (ex. "2022-01-01T00:01:02.123456Z")

        """
        self.dateStart = None
        """ Start date for the Date Range for extraction. """
        self.dateEnd = None
        """ End date for Date Renge for extraction. """
        self.period = None
        """ Period for extraction. """
        self.periodFrom = None
        """ Period start range for extraction. """
        self.periodTo = None
        """ Period end range for extraction. """
        self.relativeInterval = None
        """ Relative Interval for extraction. """