from Query.Config.VersionsRangeSelectionConfig import VersionsRangeSelectionConfig
class VersionSelectionConfig:
    def __init__(self):
        self.lastN = None
        self.version = None
        self.versionsRange = VersionsRangeSelectionConfig()