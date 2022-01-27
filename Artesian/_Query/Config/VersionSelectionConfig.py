from Artesian._Query.Config.VersionsRangeSelectionConfig import VersionsRangeSelectionConfig
class VersionSelectionConfig:
    """ Class that configures the Version Selection. """
    def __init__(self):
        """ Inits for the Version Selection Configuration.
            """
        self.lastN = None
        self.version = None
        self.versionsRange = VersionsRangeSelectionConfig()