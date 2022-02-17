class MostRecentSelectionConfig:
    """ Class for Most Recent Selection Configuration.
           
           Attributes:
               dateStart: start date for most recent selection.
               dateEnd: end date for most recent selection.
               period: period for most recent selection.
               periodFrom: period start for most recent selection.
               periodTo: period end for most recent selection.
    """
    def __init__(self) -> None:
        """ Inits for the Most Recent Selection Configuration. """
        self.dateStart = None
        """ Start date for most recent selection. (ISO format)"""
        self.dateEnd = None
        """ End date for most recent selection. (ISO format)"""
        self.period = None
        """ Period for most recent selection. (ISO format)"""
        self.periodFrom = None
        """ Period start for most recent selection. (ISO format)"""
        self.periodTo = None
        """ Period end for most recent selection. (ISO format)"""