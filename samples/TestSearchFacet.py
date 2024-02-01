from Artesian import ArtesianConfig
from Artesian.MarketData import *

cfg = ArtesianConfig("https://arkive.artesian.cloud/tenantName/", "APIKey")
mkdservice = MarketDataService(cfg)

res = (
    mkdservice.searchFacet(1, 1, "Riconsegnato_", filters=[
        {"Key": "ProviderName", "Value": ["SNAM", "France"]}
        ], sorts=["MarketDataId asc"], doNotLoadAdditionalInfo=False)
)

print(res)
print("Test completed")
