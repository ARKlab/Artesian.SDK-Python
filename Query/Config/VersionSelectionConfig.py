from Query.Config.LastOfSelectionConfig import LastOfSelectionConfig
class VersionSelectionConfig:
    def __init__(self):
        self.lastN = None
        self.version = None
        self.lastOf = LastOfSelectionConfig()