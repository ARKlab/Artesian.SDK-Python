class MostRecentSelectionConfig:
    """ Class for Most Recent Selection Configuration.
          
          The DateTime is set in ISO8601 format

           versionFrom:
             the start version timestamp in ISO8601 (ex. "2022-01-01T00:01:02.123456")
          downloadedAt:
             the timestamp of the data in ISO8601 UTC (ex. "2022-01-01T00:01:02.123456Z")
             
           Attributes:
               dateStart: start date for most recent selection.
               dateEnd: end date for most recent selection.
               period: period for most recent selection.
               periodFrom: period start for most recent selection.
               periodTo: period end for most recent selection.
          """
    def __init__(self):
        """ Inits for the Most Recent Selection Configuration. """
        self.dateStart = None
        """ Start date for most recent selection. """
        self.dateEnd = None
        """ End date for most recent selection. """
        self.period = None
        """ Period for most recent selection. """
        self.periodFrom = None
        """ Period start for most recent selection. """
        self.periodTo = None
        """ Period end for most recent selection. """