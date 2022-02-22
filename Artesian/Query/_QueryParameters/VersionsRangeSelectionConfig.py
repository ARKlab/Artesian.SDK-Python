class VersionsRangeSelectionConfig:
    """ The class Configures the Version Range Selection.
    
        Attributes:
            dateStart: start date for the version range selection configuration.
            dateEnd: end date for the version range selection configuration.
            period: period range for the version range selection configuration.
            periodFrom: period start for the version range selection configuration.
            periodTo: period end for the version range selection configuration.
    """
            
    def __init__(self, dateStart: str=None, dateEnd: str=None, period: str=None, periodFrom: str=None, periodTo: str=None) -> None:
        """ Inits for the Versions Range Selection Configuration. """
        
        self.dateStart = dateStart
        """ Start date for the versions range selection configuration. (ISO format)"""
        self.dateEnd = dateEnd
        """ End date for the versions range selection configuration. (ISO format)"""
        self.period = period
        """ Period for the versions range selection configuration. (ISO format)"""
        self.periodFrom = periodFrom
        """ Period Start for the versions range selection configuration. (ISO format)"""
        self.periodTo = periodTo
        """ Period End for the versions range selection configuration. (ISO format)"""