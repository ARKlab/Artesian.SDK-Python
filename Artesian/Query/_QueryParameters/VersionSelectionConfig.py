from .VersionsRangeSelectionConfig import VersionsRangeSelectionConfig
class VersionSelectionConfig:
    """ The class configures the Version Selection. 
    
        Attributes:
            lastN: last N for version selection.
            version: for the selection
            versionRange: based on the version range selection configuration.
    """   
    def __init__(self, lastN: int  =None, version: str  =None, versionsRange: str  =None) -> None:
        """ Inits for the Version Selection Configuration. """
        self.lastN = lastN
        self.version = version
        self.versionsRange = VersionsRangeSelectionConfig()