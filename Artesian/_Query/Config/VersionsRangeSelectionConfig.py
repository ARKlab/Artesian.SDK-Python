class VersionsRangeSelectionConfig:
    """ The class Configures the Version Range Selection.
    
        Attributes:
            dateStart: start date for the version range selection configuration.
            dateEnd: end date for the version range selection configuration.
            period: period range for the version range selection configuration.
            periodFrom: period start for the version range selection configuration.
            periodTo: period end for the version range selection configuration.
    """
            
    def __init__(self):
        """ Inits for the Versions Range Selection Configuration. """
        
        self.dateStart = None
        """ Start date for the versions range selection configuration. (ISO format)"""
        self.dateEnd = None
        """ End date for the versions range selection configuration. (ISO format)"""
        self.period = None
        """ Period for the versions range selection configuration. (ISO format)"""
        self.periodFrom = None
        """ Period Start for the versions range selection configuration. (ISO format)"""
        self.periodTo = None
        """ Period End for the versions range selection configuration. (ISO format)"""